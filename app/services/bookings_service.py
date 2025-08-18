from sqlalchemy.orm import Session
from app.db import models, schemas

def create_booking(db: Session, booking: schemas.BookingCreate):
    # Simple booking creation - frontend manages session_id
    new_booking = models.Booking(
        booking_type=booking.booking_type,
        item_id=booking.item_id,
        details=booking.details,
        price=booking.price,
        user_id=booking.user_id,
        session_id=booking.session_id  # Frontend sends this for guest bookings
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

def list_bookings(db: Session, user_id: int = None, session_id: str = None):
    if user_id is not None:
        # Return bookings for specific user
        return db.query(models.Booking).filter(models.Booking.user_id == user_id).all()
    elif session_id is not None:
        # Return bookings for specific guest session
        return db.query(models.Booking).filter(
            models.Booking.user_id.is_(None),
            models.Booking.session_id == session_id
        ).all()
    else:
        # Return all guest bookings (all sessions combined)
        return db.query(models.Booking).filter(models.Booking.user_id.is_(None)).all()

def list_all_bookings(db: Session):
    # Return all bookings (both guest and user bookings)
    return db.query(models.Booking).all()
