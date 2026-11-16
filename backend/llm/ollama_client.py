import os
import httpx
from typing import Dict, Any, Optional
from backend.config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    LLM_PROVIDER,
    GEMINI_API_KEY,
    GEMINI_MODEL
)
from backend.llm.prompts import SYSTEM_GROUNDING_PROMPT
from backend.utils.logging_config import logger

class OllamaClient:
    """Unified LLM client supporting local Ollama and Google Cloud (Gemini API)."""

    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = OLLAMA_MODEL):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = 60.0  # seconds
        self.provider = LLM_PROVIDER.lower()
        self.gemini_key = GEMINI_API_KEY
        self.gemini_model = GEMINI_MODEL

    def check_health(self) -> Dict[str, Any]:
        """Check LLM provider availability."""
        # Check Gemini if configured or if key is provided
        if self.provider == "gemini" or (self.gemini_key and self.provider != "ollama"):
            if not self.gemini_key:
                return {
                    "status": "config_error",
                    "provider": "gemini",
                    "model": self.gemini_model,
                    "model_available": False,
                    "error": "GEMINI_API_KEY is not set in environment."
                }
            return {
                "status": "online",
                "provider": "google_gemini",
                "model": self.gemini_model,
                "model_available": True,
                "available_models": [self.gemini_model, "gemini-1.5-flash", "gemini-2.0-flash"]
            }

        # Otherwise check Ollama
        try:
            with httpx.Client(timeout=5.0) as client:
                res = client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    models_data = res.json().get("models", [])
                    available_models = [m.get("name") for m in models_data]
                    model_found = any(self.model in m or m.startswith(self.model) for m in available_models)
                    return {
                        "status": "online",
                        "provider": "ollama",
                        "model": self.model,
                        "model_available": model_found,
                        "available_models": available_models
                    }
        except Exception as e:
            logger.warning(f"Ollama health check failed: {str(e)}")
        
        # If Ollama is offline but Gemini key exists, report Gemini ready
        if self.gemini_key:
            return {
                "status": "online",
                "provider": "google_gemini",
                "model": self.gemini_model,
                "model_available": True,
                "note": "Using Google Gemini fallback (Ollama offline)"
            }

        return {
            "status": "offline",
            "provider": "ollama",
            "model": self.model,
            "model_available": False,
            "error": "Ollama server is unreachable at " + self.base_url
        }

    def _generate_gemini(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        """Generate response using Google Gemini REST API."""
        if not self.gemini_key:
            return {"success": False, "error": "GEMINI_API_KEY is missing.", "answer": ""}
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent?key={self.gemini_key}"
        payload: Dict[str, Any] = {
            "contents": [
                {"role": "user", "parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.9,
                "maxOutputTokens": 2048
            }
        }
        if system:
            payload["systemInstruction"] = {
                "parts": [{"text": system}]
            }

        try:
            logger.info(f"Generating answer with Google Gemini model '{self.gemini_model}'...")
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        text = "".join([p.get("text", "") for p in parts]).strip()
                        return {"success": True, "answer": text}
                    return {"success": False, "error": "Empty response from Gemini API.", "answer": ""}
                else:
                    return {"success": False, "error": f"Gemini API error {res.status_code}: {res.text}", "answer": ""}
        except Exception as e:
            logger.error(f"Gemini API request failed: {e}")
            return {"success": False, "error": f"Gemini error: {str(e)}", "answer": ""}

    def generate(self, prompt: str, system: Optional[str] = None) -> Dict[str, Any]:
        """Generate response from active provider (Gemini or Ollama)."""
        # If explicitly Gemini or if Gemini key is set and provider is gemini
        if self.provider == "gemini":
            return self._generate_gemini(prompt, system)

        # Try Ollama first
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9
            }
        }
        if system:
            payload["system"] = system

        try:
            logger.info(f"Sending prompt to Ollama model '{self.model}'...")
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    response_text = data.get("response", "").strip()
                    if not response_text:
                        return {"success": False, "error": "Received empty response from Ollama model.", "answer": ""}
                    return {"success": True, "answer": response_text}
                elif response.status_code == 404:
                    # Model missing in Ollama, try Gemini fallback if key exists
                    if self.gemini_key:
                        logger.info("Ollama model not found; falling back to Google Gemini...")
                        return self._generate_gemini(prompt, system)
                    return {
                        "success": False,
                        "error": f"Model '{self.model}' not found in Ollama. Please run: 'ollama pull {self.model}'",
                        "answer": ""
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Ollama returned HTTP {response.status_code}: {response.text}",
                        "answer": ""
                    }
        except (httpx.ConnectError, httpx.TimeoutException) as conn_err:
            # If Ollama is offline but Gemini is available, use Gemini
            if self.gemini_key:
                logger.info(f"Ollama unavailable ({conn_err}); falling back to Google Gemini...")
                return self._generate_gemini(prompt, system)
            
            logger.error(f"Ollama connection error: {conn_err}")
            return {
                "success": False,
                "error": "SevaAI cannot connect to Ollama. Please ensure Ollama is running at " + self.base_url,
                "answer": ""
            }
        except Exception as e:
            logger.error(f"Unexpected error calling LLM API: {str(e)}")
            return {
                "success": False,
                "error": f"Error communicating with LLM: {str(e)}",
                "answer": ""
            }

    def generate_grounded_answer(self, question: str, context: str) -> Dict[str, Any]:
        """Generate grounded answer using strict system prompt and retrieved context."""
        formatted_prompt = SYSTEM_GROUNDING_PROMPT.format(context=context, question=question)
        return self.generate(prompt=formatted_prompt)
