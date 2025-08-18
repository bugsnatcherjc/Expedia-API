from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import schemas
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

# === EXPEDIA-STYLE OTP AUTHENTICATION ===

@router.post("/signup/send-otp", response_model=schemas.OTPResponse)
def send_signup_otp(signup_request: schemas.UserSignupRequest, db: Session = Depends(get_db)):
    """
    Step 1: Send OTP for new user signup (Expedia-style)
    
    Frontend flow:
    1. User enters email (and optionally phone)
    2. System sends OTP to email/phone
    3. User enters OTP + completes signup details
    """
    return auth_service.send_otp_for_signup(db, signup_request)

@router.post("/signup/complete", response_model=schemas.UserResponse)
def complete_signup(signup_data: schemas.CompleteSignupRequest, db: Session = Depends(get_db)):
    """
    Step 2: Complete signup with OTP verification
    
    User provides:
    - email
    - username 
    - password
    - otp_code (received via email/SMS)
    """
    return auth_service.complete_signup_with_otp(db, signup_data)

@router.post("/login/send-otp", response_model=schemas.OTPResponse)
def send_login_otp(login_request: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Step 1: Send OTP for existing user login (Expedia-style)
    
    Frontend flow:
    1. User enters email
    2. System sends OTP to registered email/phone
    3. User enters OTP to login
    """
    return auth_service.send_otp_for_login(db, login_request)

@router.post("/login/verify-otp")
def verify_login_otp(login_data: schemas.LoginWithOTPRequest, db: Session = Depends(get_db)):
    """
    Step 2: Login with OTP verification
    
    User provides:
    - email
    - otp_code (received via email/SMS)
    """
    return auth_service.login_with_otp(db, login_data)

# === LEGACY ENDPOINTS (for backward compatibility) ===

@router.post("/signup", response_model=schemas.UserResponse)
def signup_legacy(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Legacy signup without OTP - use /signup/send-otp instead"""
    return auth_service.create_user(db, user)

@router.post("/login")
def login_legacy(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Legacy login without OTP - use /login/send-otp instead"""
    return auth_service.login_user(db, credentials)
    