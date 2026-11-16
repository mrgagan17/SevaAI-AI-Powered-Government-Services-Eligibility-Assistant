import sys
import os
import shutil
import httpx

# Add parent dir to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL, DOCUMENTS_DIR, CHROMA_PATH

def check_setup():
    print("=========================================")
    print("         SevaAI Setup Check              ")
    print("=========================================\n")

    all_ok = True

    # 1. Check Python version
    py_ver = sys.version_info
    if py_ver.major == 3 and py_ver.minor >= 10:
        print(f"[OK] Python installed ({py_ver.major}.{py_ver.minor}.{py_ver.micro})")
    else:
        print(f"[X] Python version {py_ver.major}.{py_ver.minor} detected. Recommend Python 3.11+")
        all_ok = False

    # 2. Check required packages
    packages = ["fastapi", "uvicorn", "pydantic", "pymupdf", "chromadb", "sentence_transformers", "sqlalchemy", "httpx", "jwt", "bcrypt"]
    missing_pkgs = []
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            missing_pkgs.append(pkg)

    if not missing_pkgs:
        print("[OK] All required Python packages installed")
    else:
        print(f"[X] Missing Python packages: {', '.join(missing_pkgs)}")
        print("  Run: pip install -r requirements.txt")
        all_ok = False

    # 3. Check data directories
    os.makedirs(DOCUMENTS_DIR, exist_ok=True)
    os.makedirs(CHROMA_PATH, exist_ok=True)
    print("[OK] Data directories verified")

    # 4. Check Embedding model
    try:
        from sentence_transformers import SentenceTransformer
        print(f"[OK] Embedding library ready")
    except Exception as e:
        print(f"[X] Sentence-transformers error: {e}")
        all_ok = False

    # 5. Check Ollama
    ollama_cmd = shutil.which("ollama")
    if ollama_cmd:
        print(f"[OK] Ollama CLI found ({ollama_cmd})")
    else:
        print("[!] Ollama CLI binary not found in system PATH (may still be running as a service)")

    # 6. Check Ollama Server Connection & Model
    try:
        with httpx.Client(timeout=3.0) as client:
            res = client.get(f"{OLLAMA_BASE_URL}/api/tags")
            if res.status_code == 200:
                print(f"[OK] Ollama server online at {OLLAMA_BASE_URL}")
                models = [m.get("name") for m in res.json().get("models", [])]
                model_match = any(OLLAMA_MODEL in m or m.startswith(OLLAMA_MODEL) for m in models)
                if model_match:
                    print(f"[OK] Model '{OLLAMA_MODEL}' available in Ollama")
                else:
                    print(f"[X] Model '{OLLAMA_MODEL}' not found in Ollama. Found: {models}")
                    print(f"  Run: ollama pull {OLLAMA_MODEL}")
                    all_ok = False
            else:
                print(f"[X] Ollama returned status {res.status_code}")
                all_ok = False
    except Exception:
        print(f"[!] Ollama server is offline at {OLLAMA_BASE_URL}")
        print(f"  Note: Ollama can be launched with 'ollama serve' and model pulled via 'ollama pull {OLLAMA_MODEL}'")

    print("\n-----------------------------------------")
    if all_ok:
        print("SevaAI setup is verified and ready!")
    else:
        print("SevaAI backend is installed. Check any warnings/offline components above.")
    print("-----------------------------------------")

if __name__ == "__main__":
    check_setup()
