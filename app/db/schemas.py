# === User Trip Planner Schemas ===
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import json

class UserTripCreate(BaseModel):
    email: EmailStr
    trip_id: int
    trip_name: str
    destination: str
    start_date: str
    end_date: str
    trip_type: Optional[str] = None
    invite_flag: Optional[bool] = False
    created_for_you: Optional[bool] = False
    notes: Optional[str] = None
    status: Optional[str] = "current"  # current, past, canceled

class UserTripResponse(BaseModel):
    id: int
    trip_id: int
    trip_name: str
    destination: str
    start_date: str
    end_date: str
    trip_type: Optional[str]
    invite_flag: bool
    created_for_you: bool
    notes: Optional[str]
    image: Optional[str]
    status: str
    created_at: datetime
    class Config:
        orm_mode = True

class UserTripListResponse(BaseModel):
    trips: List[UserTripResponse]



class TravelerCreate(BaseModel):
    email: EmailStr
    name: str
    frequent_flyer: Optional[str] = None
    membership: Optional[str] = None
    personal_info: Optional[dict] = None
    flight_preference: Optional[dict] = None
    passports: Optional[list] = None
    tsa_info: Optional[dict] = None

class TravelerResponse(BaseModel):
    id: int
    name: str
    frequent_flyer: Optional[str]
    membership: Optional[str]
    personal_info: Optional[dict]
    flight_preference: Optional[dict]
    passports: Optional[list]
    tsa_info: Optional[dict]
    created_at: datetime

class TravelerListResponse(BaseModel):
    travelers: List[TravelerResponse]


class PaymentMethodCreate(BaseModel):
    email: EmailStr
    card_type: str
    cardholder: str
    card_number: str  # will only store last4
    exp_month: str
    exp_year: str
    csc: str
    billing_address: Optional[str] = None

class PaymentMethodResponse(BaseModel):
    id: int
    card_type: str
    cardholder: str
    last4: str
    exp_month: str
    exp_year: str
    csc: str
    billing_address: Optional[str]
    created_at: datetime

class PaymentMethodListResponse(BaseModel):
    payment_methods: List[PaymentMethodResponse]

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
    bio: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    accessibility_note: Optional[str] = None
    emergency_contact: Optional[str] = None
    address: Optional[str] = None
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
    bio: Optional[str] = None
    dob: Optional[str] = None
    gender: Optional[str] = None
    accessibility_note: Optional[str] = None
    emergency_contact: Optional[str] = None
    address: Optional[str] = None

class UpdateUserResponse(BaseModel):
    message: str
    user: UserResponse

# === Profile Read Schema ===
class ProfileResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    bio: Optional[str]
    dob: Optional[str]
    gender: Optional[str]
    accessibility_note: Optional[str]
    emergency_contact: Optional[str]
    address: Optional[str]
    created_at: datetime

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
