# SevaAI LLM Package
from backend.llm.ollama_client import OllamaClient
from backend.llm.prompts import SYSTEM_GROUNDING_PROMPT, ELIGIBILITY_EVALUATION_PROMPT

__all__ = ["OllamaClient", "SYSTEM_GROUNDING_PROMPT", "ELIGIBILITY_EVALUATION_PROMPT"]
