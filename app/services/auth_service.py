from sqlalchemy.orm import Session
from app.db import models, schemas
from app.db.models import Traveler, PaymentMethod
from fastapi import HTTPException
from datetime import datetime, timedelta
from app.core.security import get_password_hash, verify_password, create_access_token
import random
import string
import json

def add_traveler(db: Session, payload: schemas.TravelerCreate):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Dummy data for missing fields
    personal_info = payload.personal_info or {
        "dob": "1990-01-01",
        "gender": "male",
        "nationality": "USA"
    }
    flight_preference = payload.flight_preference or {
        "seat": "aisle",
        "meal": "vegetarian",
        "class": "economy"
    }
    passports = payload.passports or [
        {"number": "X1234567", "country": "USA", "expiry": "2030-12-31"}
    ]
    tsa_info = payload.tsa_info or {
        "tsa_precheck": True,
        "known_traveler_number": "987654321"
    }
    traveler = Traveler(
        user_id=user.id,
        name=payload.name,
        frequent_flyer=payload.frequent_flyer or "AA123456",
        membership=payload.membership or "Gold",
        personal_info=json.dumps(personal_info),
        flight_preference=json.dumps(flight_preference),
        passports=json.dumps(passports),
        tsa_info=json.dumps(tsa_info)
    )
    db.add(traveler)
    db.commit()
    db.refresh(traveler)
    return {
        "id": traveler.id,
        "name": traveler.name,
        "frequent_flyer": traveler.frequent_flyer,
        "membership": traveler.membership,
        "personal_info": personal_info,
        "flight_preference": flight_preference,
        "passports": passports,
        "tsa_info": tsa_info,
        "created_at": traveler.created_at
    }

def list_travelers(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    travelers = db.query(Traveler).filter(Traveler.user_id == user.id).all()
    result = []
    for t in travelers:
        result.append({
            "id": t.id,
            "name": t.name,
            "frequent_flyer": t.frequent_flyer,
            "membership": t.membership,
            "personal_info": json.loads(t.personal_info) if t.personal_info else None,
            "flight_preference": json.loads(t.flight_preference) if t.flight_preference else None,
            "passports": json.loads(t.passports) if t.passports else None,
            "tsa_info": json.loads(t.tsa_info) if t.tsa_info else None,
            "created_at": t.created_at
        })
    return {"travelers": result}

def remove_traveler(db: Session, email: str, traveler_id: int):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    traveler = db.query(Traveler).filter(Traveler.user_id == user.id, Traveler.id == traveler_id).first()
    if not traveler:
        raise HTTPException(status_code=404, detail="Traveler not found")
    db.delete(traveler)
    db.commit()
    return {"message": "Traveler removed"}
from app.db.models import PaymentMethod
def add_payment_method(db: Session, payload: schemas.PaymentMethodCreate):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Only store last 4 digits
    last4 = payload.card_number[-4:]
    pm = PaymentMethod(
        user_id=user.id,
        card_type=payload.card_type,
        cardholder=payload.cardholder,
        last4=last4,
        exp_month=payload.exp_month,
        exp_year=payload.exp_year,
        csc=payload.csc,
        billing_address=payload.billing_address
    )
    db.add(pm)
    db.commit()
    db.refresh(pm)
    return {
        "id": pm.id,
        "card_type": pm.card_type,
        "cardholder": pm.cardholder,
        "last4": pm.last4,
        "exp_month": pm.exp_month,
        "exp_year": pm.exp_year,
        "csc": pm.csc,
        "billing_address": pm.billing_address,
        "created_at": pm.created_at
    }

def list_payment_methods(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    methods = db.query(PaymentMethod).filter(PaymentMethod.user_id == user.id).all()
    return {
        "payment_methods": [
            {
                "id": pm.id,
                "card_type": pm.card_type,
                "cardholder": pm.cardholder,
                "last4": pm.last4,
                "exp_month": pm.exp_month,
                "exp_year": pm.exp_year,
                "csc": pm.csc,
                "billing_address": pm.billing_address,
                "created_at": pm.created_at
            }
            for pm in methods
        ]
    }
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
                "bio": existing_user.bio,
                "dob": existing_user.dob,
                "gender": existing_user.gender,
                "accessibility_note": existing_user.accessibility_note,
                "emergency_contact": existing_user.emergency_contact,
                "address": existing_user.address,
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
                "bio": new_user.bio,
                "dob": new_user.dob,
                "gender": new_user.gender,
                "accessibility_note": new_user.accessibility_note,
                "emergency_contact": new_user.emergency_contact,
                "address": new_user.address,
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

    # Profile fields
    if payload.bio is not None:
        user.bio = payload.bio.strip() or None
        updated = True
    if payload.dob is not None:
        user.dob = payload.dob.strip() or None
        updated = True
    if payload.gender is not None:
        user.gender = payload.gender.strip() or None
        updated = True
    if payload.accessibility_note is not None:
        user.accessibility_note = payload.accessibility_note.strip() or None
        updated = True
    if payload.emergency_contact is not None:
        user.emergency_contact = payload.emergency_contact.strip() or None
        updated = True
    if payload.address is not None:
        user.address = payload.address.strip() or None
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
            "bio": user.bio,
            "dob": user.dob,
            "gender": user.gender,
            "accessibility_note": user.accessibility_note,
            "emergency_contact": user.emergency_contact,
            "address": user.address,
            "phone": user.phone,
            "is_verified": user.is_verified,
            "created_at": user.created_at
        }
    }

def get_profile(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "bio": user.bio,
        "dob": user.dob,
        "gender": user.gender,
        "accessibility_note": user.accessibility_note,
        "emergency_contact": user.emergency_contact,
        "address": user.address,
        "created_at": user.created_at
    }
