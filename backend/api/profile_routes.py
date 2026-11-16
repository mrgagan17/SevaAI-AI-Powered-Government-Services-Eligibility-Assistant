from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.database_models import User
from backend.models.schemas import ProfileCreate, ProfileResponse, ProfileBase
from backend.services.profile_service import ProfileService
from backend.utils.auth_utils import get_current_user

router = APIRouter(prefix="/api/profile", tags=["Profile"])

@router.get("", response_model=ProfileResponse)
def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetch profile strictly for current authenticated citizen user."""
    profile = ProfileService.get_profile(db, user_id=current_user.id)
    if not profile:
        profile = ProfileService.create_or_update_profile(
            db, ProfileCreate(name=current_user.full_name), user_id=current_user.id
        )
    return profile

@router.post("", response_model=ProfileResponse)
def create_user_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update profile strictly for current authenticated citizen user."""
    return ProfileService.create_or_update_profile(db, profile_data, user_id=current_user.id)

@router.put("", response_model=ProfileResponse)
def update_user_profile(
    profile_data: ProfileBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update profile fields strictly for current authenticated citizen user."""
    return ProfileService.create_or_update_profile(db, profile_data, user_id=current_user.id)
