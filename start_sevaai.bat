@echo off
TITLE SevaAI - Government Services & Eligibility Assistant
echo ===================================================
echo             Starting SevaAI Application
echo ===================================================
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo [!] Virtual environment not found. Creating .venv...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo Running setup check...
python scripts\check_setup.py

echo.
echo Starting SevaAI Backend (FastAPI on http://localhost:8000)...
start "SevaAI Backend" cmd /k ".venv\Scripts\uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo Starting SevaAI Frontend (Vite on http://localhost:5173)...
start "SevaAI Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo SevaAI is launching!
echo Backend API  : http://localhost:8000 (Docs at /docs)
echo Web App UI   : http://localhost:5173
echo ===================================================
echo.
pause
