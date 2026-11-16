from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.database_models import User, UserProfile
from backend.models.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from backend.utils.auth_utils import hash_password, verify_password, create_access_token, get_current_user
from backend.utils.logging_config import logger

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new citizen user account."""
    email_clean = user_data.email.strip().lower()
    if not email_clean or "@" not in email_clean:
        raise HTTPException(status_code=400, detail="Please provide a valid email address.")
    
    if len(user_data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")

    existing_user = db.query(User).filter(User.email == email_clean).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    hashed_pw = hash_password(user_data.password)
    user_name = user_data.full_name.strip() if user_data.full_name else "Citizen"

    new_user = User(
        email=email_clean,
        password_hash=hashed_pw,
        full_name=user_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Initialize a personal profile for the user
    user_profile = UserProfile(
        user_id=new_user.id,
        name=user_name
    )
    db.add(user_profile)
    db.commit()

    token = create_access_token(data={"sub": str(new_user.id), "email": new_user.email})
    logger.info(f"Registered new user account: {new_user.email}")

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            full_name=new_user.full_name,
            created_at=new_user.created_at.isoformat() if new_user.created_at else None
        )
    )

@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate citizen user and return access token."""
    email_clean = login_data.email.strip().lower()
    user = db.query(User).filter(User.email == email_clean).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account has been disabled."
        )

    token = create_access_token(data={"sub": str(user.id), "email": user.email})
    logger.info(f"User logged in successfully: {user.email}")

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at.isoformat() if user.created_at else None
        )
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile details."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        created_at=current_user.created_at.isoformat() if current_user.created_at else None
    )

