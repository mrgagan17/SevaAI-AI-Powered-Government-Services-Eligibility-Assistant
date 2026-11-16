import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.database import init_db
from backend.api import main_router, chat_router, document_router, profile_router, auth_router
from backend.config import SERVE_STATIC, STATIC_DIR
from backend.utils.logging_config import logger

# Initialize database tables & auto-migrations
init_db()

app = FastAPI(
    title="SevaAI API",
    description="AI-Powered Government Services & Eligibility Assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for flexible hosting & local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(main_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(document_router)
app.include_router(profile_router)

# Serve compiled frontend in production (Single-container Google Cloud Run deployment)
if SERVE_STATIC and STATIC_DIR.exists():
    assets_dir = STATIC_DIR / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Keep API and doc endpoints unobstructed
        if full_path.startswith("api/") or full_path in ("docs", "redoc", "openapi.json", "health"):
            raise HTTPException(status_code=404, detail="Endpoint not found")
        
        file_path = STATIC_DIR / full_path
        if file_path.is_file():
            return FileResponse(file_path)
            
        index_file = STATIC_DIR / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
            
        return {"name": "SevaAI API", "status": "running"}

@app.on_event("startup")
def startup_event():
    logger.info("SevaAI FastAPI backend application started.")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
