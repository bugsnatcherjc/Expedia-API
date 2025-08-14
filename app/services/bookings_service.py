from sqlalchemy.orm import Session
from app.db import models, schemas

def create_booking(db: Session, booking: schemas.BookingCreate):
    new_booking = models.Booking(
        booking_type=booking.booking_type,
        item_id=booking.item_id,
        details=booking.details,
        price=booking.price,
        user_id=booking.user_id
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

def list_bookings(db: Session, user_id: int):
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).all()
