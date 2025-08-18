from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # hashed or plain for now
    phone = Column(String, nullable=True)  # For OTP
    is_verified = Column(Boolean, default=False)  # Email/phone verification status
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="user")

class OTPCode(Base):
    __tablename__ = "otp_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    otp_code = Column(String, nullable=False)
    otp_type = Column(String, nullable=False)  # 'signup', 'login', 'password_reset'
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_type = Column(String, nullable=False)  # stay, flight, car, etc.
    item_id = Column(Integer, nullable=False)  # ID from mock data
    details = Column(String, nullable=True)  # JSON/text string of booking info
    price = Column(Float, nullable=True)
    booked_at = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String, nullable=True)  # For guest bookings tracking

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Made nullable for guest bookings
    user = relationship("User", back_populates="bookings")
