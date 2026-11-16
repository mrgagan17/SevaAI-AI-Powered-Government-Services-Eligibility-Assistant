# SevaAI API Routes Package
from backend.api.routes import router as main_router
from backend.api.chat_routes import router as chat_router
from backend.api.document_routes import router as document_router
from backend.api.profile_routes import router as profile_router
from backend.api.auth_routes import router as auth_router

__all__ = ["main_router", "chat_router", "document_router", "profile_router", "auth_router"]
