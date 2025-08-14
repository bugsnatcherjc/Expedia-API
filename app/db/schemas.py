from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    class Config:
        orm_mode = True

class BookingCreate(BaseModel):
    booking_type: str
    item_id: int
    details: Optional[str] = None
    price: Optional[float] = None
    user_id: int

class BookingResponse(BaseModel):
    id: int
    booking_type: str
    item_id: int
    details: Optional[str]
    price: Optional[float]
    booked_at: datetime
    user_id: int
    class Config:
        orm_mode = True
