from typing import Optional
from sqlalchemy.orm import Session
from backend.models.database_models import UserProfile
from backend.models.schemas import ProfileCreate, ProfileBase
from backend.utils.logging_config import logger

class ProfileService:
    """Service layer managing UserProfile database persistence."""

    @staticmethod
    def get_profile(db: Session, user_id: Optional[int] = None) -> Optional[UserProfile]:
        """Fetch user profile scoped to user_id, or guest profile."""
        if user_id is not None:
            profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            if profile:
                return profile
            return None
        
        # Guest profile: find unassigned profile, or return first
        guest_profile = db.query(UserProfile).filter(UserProfile.user_id == None).first()
        if not guest_profile:
            guest_profile = db.query(UserProfile).first()
        return guest_profile

    @staticmethod
    def create_or_update_profile(db: Session, profile_data: ProfileBase, user_id: Optional[int] = None) -> UserProfile:
        """Create or update citizen profile for user_id or guest."""
        existing = None
        if user_id is not None:
            existing = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        else:
            existing = db.query(UserProfile).filter(UserProfile.user_id == None).first()
            if not existing:
                existing = db.query(UserProfile).first()
        
        if existing:
            for key, value in profile_data.model_dump(exclude_unset=True).items():
                if key != "user_id":
                    setattr(existing, key, value)
            if user_id is not None and existing.user_id is None:
                existing.user_id = user_id
            db.commit()
            db.refresh(existing)
            logger.info(f"Updated profile for '{existing.name}' (user_id={user_id})")
            return existing
        else:
            dump_data = profile_data.model_dump()
            dump_data["user_id"] = user_id
            new_profile = UserProfile(**dump_data)
            db.add(new_profile)
            db.commit()
            db.refresh(new_profile)
            logger.info(f"Created new profile for '{new_profile.name}' (user_id={user_id})")
            return new_profile
