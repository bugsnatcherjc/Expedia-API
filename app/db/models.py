from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # hashed or plain for now

    bookings = relationship("Booking", back_populates="user")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_type = Column(String, nullable=False)  # stay, flight, car, etc.
    item_id = Column(Integer, nullable=False)  # ID from mock data
    details = Column(String, nullable=True)  # JSON/text string of booking info
    price = Column(Float, nullable=True)
    booked_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="bookings")
