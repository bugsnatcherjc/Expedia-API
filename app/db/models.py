from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
# === UserTrip Model ===
class UserTrip(Base):
    __tablename__ = "user_trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id = Column(Integer, nullable=False)  # ID from trips_list.json
    trip_name = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    trip_type = Column(String, nullable=True)  # flight, hotel, etc.
    invite_flag = Column(Boolean, default=False)
    created_for_you = Column(Boolean, default=False)
    notes = Column(String, nullable=True)
    image = Column(String, nullable=True)  # URL to trip image
    status = Column(String, nullable=False, default="current")  # current, past, canceled
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


# === Traveler Model ===
class Traveler(Base):
    __tablename__ = "travelers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    frequent_flyer = Column(String, nullable=True)
    membership = Column(String, nullable=True)
    personal_info = Column(String, nullable=True)  # JSON string
    flight_preference = Column(String, nullable=True)  # JSON string
    passports = Column(String, nullable=True)  # JSON string
    tsa_info = Column(String, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
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
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)  # For OTP
    # Profile fields
    bio = Column(String, nullable=True)
    dob = Column(String, nullable=True)  # ISO date string (YYYY-MM-DD)
    gender = Column(String, nullable=True)
    accessibility_note = Column(String, nullable=True)
    emergency_contact = Column(String, nullable=True)  # store as plain text for now
    address = Column(String, nullable=True)  # plain text or JSON string
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

# === Payment Method Model ===
class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_type = Column(String, nullable=False)  # e.g. Visa, Mastercard
    cardholder = Column(String, nullable=False)
    last4 = Column(String, nullable=False)      # last 4 digits
    exp_month = Column(String, nullable=False)
    exp_year = Column(String, nullable=False)
    csc = Column(String, nullable=False)  # Card Security Code
    billing_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
