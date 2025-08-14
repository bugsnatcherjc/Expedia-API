from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import schemas
from app.services import bookings_service

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/create", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return bookings_service.create_booking(db, booking)

@router.get("/list", response_model=List[schemas.BookingResponse])
def list_bookings(user_id: int, db: Session = Depends(get_db)):
    return bookings_service.list_bookings(db, user_id)
