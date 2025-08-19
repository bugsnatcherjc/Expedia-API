from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# === User Authentication Schemas ===
class UserSignupRequest(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    
class OTPVerificationRequest(BaseModel):
    email: EmailStr
    otp_code: str
    otp_type: str  # 'signup', 'login', 'password_reset'

class CompleteSignupRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    otp_code: str

class LoginRequest(BaseModel):
    email: EmailStr
    
class LoginWithOTPRequest(BaseModel):
    email: EmailStr
    otp_code: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    is_verified: bool
    created_at: datetime
    class Config:
        orm_mode = True

class OTPResponse(BaseModel):
    message: str
    email: str
    otp_code: str  # Only for development - remove in production
    expires_in_minutes: int
    action_type: str = "unified"  # "login", "registration", "unified"
    user_exists: bool = False

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict  # UserResponse data
    action_type: str  # "login" or "registration"
    message: str

# === User Profile Update Schemas ===
class UpdateUserRequest(BaseModel):
    # Used after OTP flows
    email: EmailStr
    # Optional, frontend can send in separate screens
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None  # set or update password
    phone: Optional[str] = None     # update phone after login

class UpdateUserResponse(BaseModel):
    message: str
    user: UserResponse

class BookingCreate(BaseModel):
    booking_type: str  # "flight", "stay", "car", "activity"
    item_id: int
    details: Optional[str] = None
    price: Optional[float] = None
    user_id: Optional[int] = None  # For registered users
    session_id: Optional[str] = None  # For guest bookings - frontend should generate and send this

class BookingResponse(BaseModel):
    id: int
    booking_type: str
    item_id: int
    details: Optional[str]
    price: Optional[float]
    booked_at: datetime
    user_id: Optional[int]  # Will be None for guest bookings
    session_id: Optional[str]  # Will contain frontend-generated session ID for guests
    class Config:
        orm_mode = True
