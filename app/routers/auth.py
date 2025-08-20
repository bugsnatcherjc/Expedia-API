from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import schemas
from app.services import auth_service
from pydantic import BaseModel
from fastapi import Query

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/traveler", response_model=schemas.TravelerResponse)
def add_traveler(
    payload: schemas.TravelerCreate,
    db: Session = Depends(get_db)
):
    """
    Add an additional traveler for a user.
    - The user is identified by the email field in the payload.
    - All travelers are linked to the user with this email.
    - Required: email, name.
    - Optional: frequent_flyer, membership, personal_info, flight_preference, passports, tsa_info.
    - Any missing field will be filled with dummy data.
    Example:
    {
        "email": "user@example.com",
        "name": "Alex Smith",
        "frequent_flyer": "UA987654",
        "membership": "Platinum",
        "personal_info": { "dob": "1985-07-20", "gender": "male", "nationality": "USA" },
        "flight_preference": { "seat": "window", "meal": "vegan", "class": "business" },
        "passports": [ { "number": "Y7654321", "country": "USA", "expiry": "2028-05-31" } ],
        "tsa_info": { "tsa_precheck": true, "known_traveler_number": "123456789" }
    }
    """
    try:
        return auth_service.add_traveler(db, payload)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/travelers", response_model=schemas.TravelerListResponse)
def list_travelers(
    email: str = Query(..., description="User email to list travelers for"),
    db: Session = Depends(get_db)
):
    """
    List all additional travelers for a user.
    - The user is identified by the email query parameter.
    - Returns all travelers linked to the user with this email, with all details.
    """
    try:
        return auth_service.list_travelers(db, email)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/traveler")
def remove_traveler(
    email: str = Query(..., description="User email"),
    traveler_id: int = Query(..., description="Traveler ID to remove"),
    db: Session = Depends(get_db)
):
    """
    Remove an additional traveler for a user.
    - The user is identified by the email query parameter.
    - Provide traveler_id to specify which traveler to remove.
    - Deletes the traveler linked to the user with this email.
    """
    try:
        return auth_service.remove_traveler(db, email, traveler_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
@router.post("/payment-method", response_model=schemas.PaymentMethodResponse)
def add_payment_method(
    payload: schemas.PaymentMethodCreate,
    db: Session = Depends(get_db)
):
    """
    Add a mock payment method (card) for a user.
    - The user is identified by the email field in the payload.
    - All payment methods are linked to the user with this email.
    - Allows multiple cards per user.
    - Only last 4 digits of card_number are stored.
    - Required fields: email, card_type, cardholder, card_number, exp_month, exp_year.
    - Optional: billing_address.
    Example:
    {
        "email": "user@example.com",
        "card_type": "Visa",
        "cardholder": "Jane Doe",
        "card_number": "4111111111111111",
        "exp_month": "05",
        "exp_year": "2028",
        "billing_address": "123 Main St, NY"
    }
    """
    try:
        return auth_service.add_payment_method(db, payload)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/payment-methods", response_model=schemas.PaymentMethodListResponse)
def list_payment_methods(
    email: str = Query(..., description="User email to list payment methods for"),
    db: Session = Depends(get_db)
):
    """
    List all mock payment methods (cards) for a user.
    - The user is identified by the email query parameter.
    - Returns all payment methods linked to the user with this email.
    """
    try:
        return auth_service.list_payment_methods(db, email)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

class EmailRequest(BaseModel):
    email: str

class CompleteAuthRequest(BaseModel):
    email: str
    otp_code: str


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
    
@router.get("/profile", response_model=schemas.ProfileResponse)
def get_profile(
    email: str = Query(..., description="User email to fetch profile for"),
    db: Session = Depends(get_db)
):
    try:
        return auth_service.get_profile(db, email)
    except HTTPException:
        raise
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
    