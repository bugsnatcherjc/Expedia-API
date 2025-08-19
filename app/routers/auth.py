from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import schemas
from app.services import auth_service
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

class EmailRequest(BaseModel):
    email: str

class CompleteAuthRequest(BaseModel):
    email: str
    otp_code: str

# === EXPEDIA-STYLE UNIFIED AUTHENTICATION ===

@router.post("/send-otp", response_model=schemas.OTPResponse)
def send_otp_unified(
    request: EmailRequest,
    db: Session = Depends(get_db)
):
    """
    Unified OTP sending endpoint (Expedia-style)
    - If email exists: Sends login OTP
    - If email doesn't exist: Sends registration OTP
    
    Frontend flow:
    1. User enters email
    2. System checks if user exists and sends appropriate OTP
    3. Frontend adapts UI based on user_exists flag
    """
    try:
        result = auth_service.send_otp_unified(db, request.email)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/verify-otp", response_model=schemas.AuthResponse)
def verify_otp_unified(
    request: CompleteAuthRequest,
    db: Session = Depends(get_db)
):
    """
    Unified OTP verification endpoint (Expedia-style)
    - If existing user: Logs them in
    - If new user: Automatically creates account and logs them in
    
    Only requires: email and otp_code
    """
    try:
        result = auth_service.verify_otp_unified(
            db=db,
            email=request.email,
            otp_code=request.otp_code
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/update-user", response_model=schemas.UpdateUserResponse)
def update_user_profile(
    payload: schemas.UpdateUserRequest,
    db: Session = Depends(get_db)
):
    """Update user profile fields after OTP flows.
    - Registration path: first_name, last_name, password
    - Login path: phone
    Identifies user by email (already verified via OTP previously).
    """
    try:
        return auth_service.update_user_profile(db, payload)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    