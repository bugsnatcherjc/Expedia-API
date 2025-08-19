from sqlalchemy.orm import Session
from app.db import models, schemas
from fastapi import HTTPException
from datetime import datetime, timedelta
from app.core.security import get_password_hash, verify_password, create_access_token
import random
import string

# Static OTP for development (in production, this would be sent via SMS/Email)
STATIC_OTP = "123456"
OTP_EXPIRY_MINUTES = 10

def generate_otp():
    """Generate a static OTP for development"""
    return STATIC_OTP

# === EXPEDIA-STYLE UNIFIED AUTHENTICATION ===

def send_otp_unified(db: Session, email: str):
    """
    Unified OTP sending (Expedia-style)
    - Checks if user exists
    - Sends appropriate OTP for login or registration
    """
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    
    # Generate OTP (static for development)
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    
    # Delete any existing OTP for this email
    db.query(models.OTPCode).filter(models.OTPCode.email == email).delete()
    
    # Create new OTP record
    otp_record = models.OTPCode(
        email=email,
        otp_code=otp_code,
        expires_at=expires_at,
        is_used=False,
        otp_type="unified"
    )
    db.add(otp_record)
    db.commit()
    
    # Return appropriate response based on user existence
    if existing_user:
        return {
            "message": f"OTP sent to {email} for login",
            "email": email,
            "otp_code": otp_code,  # Remove this in production
            "expires_in_minutes": OTP_EXPIRY_MINUTES,
            "action_type": "login",
            "user_exists": True
        }
    else:
        return {
            "message": f"OTP sent to {email} for registration",
            "email": email,
            "otp_code": otp_code,  # Remove this in production
            "expires_in_minutes": OTP_EXPIRY_MINUTES,
            "action_type": "registration",
            "user_exists": False
        }

def verify_otp_unified(db: Session, email: str, otp_code: str):
    """
    Unified OTP verification (Expedia-style)
    - If user exists: Log them in
    - If user doesn't exist: Auto-register and log them in
    Only requires email and OTP
    """
    # Verify OTP
    otp_record = db.query(models.OTPCode).filter(
        models.OTPCode.email == email,
        models.OTPCode.otp_code == otp_code,
        models.OTPCode.is_used == False,
        models.OTPCode.expires_at > datetime.utcnow()
    ).first()
    
    if not otp_record:
        raise ValueError("Invalid or expired OTP")
    
    # Mark OTP as used
    otp_record.is_used = True
    db.commit()
    
    # Check if user exists
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    
    if existing_user:
        # User exists - Log them in
        # Update verification status if not already verified
        if not existing_user.is_verified:
            existing_user.is_verified = True
            db.commit()
        
        # Generate access token
        access_token = create_access_token(data={"sub": existing_user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": existing_user.id,
                "username": existing_user.username,
                "email": existing_user.email,
                "first_name": existing_user.first_name,
                "last_name": existing_user.last_name,
                "phone": existing_user.phone,
                "is_verified": existing_user.is_verified
            },
            "action_type": "login",
            "message": "Login successful"
        }
    else:
        # User doesn't exist - Auto-register them
        # Generate username from email
        email_username = email.split('@')[0]
        final_username = email_username
        
        # Make username unique if needed
        counter = 1
        while db.query(models.User).filter(models.User.username == final_username).first():
            final_username = f"{email_username}_{counter}"
            counter += 1
        
        # Create new user with auto-generated data
        new_user = models.User(
            username=final_username,
            email=email,
            password=get_password_hash("temp_password"),  # Temporary password since only OTP is used
            first_name=None,
            last_name=None,
            phone=None,
            is_verified=True,  # Auto-verify since they completed OTP
            created_at=datetime.utcnow()
        )
        
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except Exception as e:
            db.rollback()
            # If there's still a conflict, use timestamp-based username
            timestamp = str(int(datetime.utcnow().timestamp()))
            fallback_username = f"{email_username}_{timestamp}"
            
            new_user.username = fallback_username
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        
        # Generate access token
        access_token = create_access_token(data={"sub": new_user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "phone": new_user.phone,
                "is_verified": new_user.is_verified
            },
            "action_type": "registration",
            "message": "Auto-registration and login successful"
        }

def update_user_profile(db: Session, payload: schemas.UpdateUserRequest):
    """Update user profile fields after OTP flows.
    - Registration flow: set first_name, last_name, password
    - Login flow: update phone
    Identifies user by email.
    """
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated = False
    if payload.first_name is not None:
        user.first_name = payload.first_name.strip() or None
        updated = True
    if payload.last_name is not None:
        user.last_name = payload.last_name.strip() or None
        updated = True
    if payload.password is not None and payload.password.strip():
        user.password = get_password_hash(payload.password)
        updated = True
    if payload.phone is not None:
        user.phone = payload.phone.strip() or None
        updated = True

    if not updated:
        raise HTTPException(status_code=400, detail="No fields to update")

    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "is_verified": user.is_verified,
            "created_at": user.created_at
        }
    }
