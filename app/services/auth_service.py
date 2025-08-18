from sqlalchemy.orm import Session
from app.db import models, schemas
from fastapi import HTTPException
from datetime import datetime, timedelta
import random
import string

# Static OTP for development (in production, this would be sent via SMS/Email)
STATIC_OTP = "123456"
OTP_EXPIRY_MINUTES = 10

def generate_otp():
    """Generate a static OTP for development"""
    return STATIC_OTP

def send_otp_for_signup(db: Session, signup_request: schemas.UserSignupRequest):
    """Send OTP for new user signup (Expedia-style)"""
    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == signup_request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered. Try logging in instead.")
    
    # Generate OTP
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    
    # Delete any existing OTP for this email
    db.query(models.OTPCode).filter(
        models.OTPCode.email == signup_request.email,
        models.OTPCode.otp_type == "signup"
    ).delete()
    
    # Create new OTP record
    otp_record = models.OTPCode(
        email=signup_request.email,
        phone=signup_request.phone,
        otp_code=otp_code,
        otp_type="signup",
        expires_at=expires_at
    )
    db.add(otp_record)
    db.commit()
    
    return {
        "message": f"OTP sent to {signup_request.email}",
        "email": signup_request.email,
        "otp_code": otp_code,  # Static OTP for development
        "expires_in_minutes": OTP_EXPIRY_MINUTES
    }

def send_otp_for_login(db: Session, login_request: schemas.LoginRequest):
    """Send OTP for existing user login (Expedia-style)"""
    # Check if user exists
    user = db.query(models.User).filter(models.User.email == login_request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found. Please sign up first.")
    
    # Generate OTP
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    
    # Delete any existing OTP for this email
    db.query(models.OTPCode).filter(
        models.OTPCode.email == login_request.email,
        models.OTPCode.otp_type == "login"
    ).delete()
    
    # Create new OTP record
    otp_record = models.OTPCode(
        email=login_request.email,
        otp_code=otp_code,
        otp_type="login",
        expires_at=expires_at
    )
    db.add(otp_record)
    db.commit()
    
    return {
        "message": f"OTP sent to {login_request.email}",
        "email": login_request.email,
        "otp_code": otp_code,  # Static OTP for development
        "expires_in_minutes": OTP_EXPIRY_MINUTES
    }

def complete_signup_with_otp(db: Session, signup_data: schemas.CompleteSignupRequest):
    """Complete user signup after OTP verification"""
    # Verify OTP
    otp_record = db.query(models.OTPCode).filter(
        models.OTPCode.email == signup_data.email,
        models.OTPCode.otp_code == signup_data.otp_code,
        models.OTPCode.otp_type == "signup",
        models.OTPCode.is_used == False,
        models.OTPCode.expires_at > datetime.utcnow()
    ).first()
    
    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    # Check if email already exists (double check)
    existing_user = db.query(models.User).filter(models.User.email == signup_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = models.User(
        username=signup_data.username,
        email=signup_data.email,
        password=signup_data.password,  # In production, hash this
        phone=otp_record.phone,
        is_verified=True
    )
    
    # Mark OTP as used
    otp_record.is_used = True
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def login_with_otp(db: Session, login_data: schemas.LoginWithOTPRequest):
    """Login user with OTP verification"""
    # Verify OTP
    otp_record = db.query(models.OTPCode).filter(
        models.OTPCode.email == login_data.email,
        models.OTPCode.otp_code == login_data.otp_code,
        models.OTPCode.otp_type == "login",
        models.OTPCode.is_used == False,
        models.OTPCode.expires_at > datetime.utcnow()
    ).first()
    
    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    # Get user
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Mark OTP as used
    otp_record.is_used = True
    db.commit()
    
    return {
        "message": "Login successful",
        "token": f"mock-token-{user.id}",  # In production, generate JWT
        "user": user
    }

# Legacy functions for backward compatibility
def create_user(db: Session, user: schemas.UserCreate):
    """Legacy function - use complete_signup_with_otp instead"""
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password,
        phone=user.phone,
        is_verified=False  # Not verified through OTP
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, credentials: schemas.UserLogin):
    """Legacy function - use login_with_otp instead"""
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": f"mock-token-{user.id}", "user": user}
