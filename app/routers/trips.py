from fastapi import HTTPException, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db import schemas
from fastapi import APIRouter, Depends

from app.services.trips_service import TripsService
from fastapi import HTTPException, status
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.db import schemas

router = APIRouter(prefix="/trips", tags=["Trips"])

# Get all trips planned by a user
@router.get("/", response_model=schemas.UserTripListResponse)
def get_user_trips(email: str, db: Session = Depends(get_db)):
    """
    Get all trips planned by a user.
    - Provide user email as query param.
    - Returns all trips linked to the user, with full details (destination, dates, type, invite, created_for_you, notes).
    """
    service = TripsService()
    trips = service.list_user_trips(db, email)
    trips_data = [schemas.UserTripResponse.from_orm(t) for t in trips]
    return {"trips": trips_data}

# Plan a trip for a user
@router.post("/plan", response_model=schemas.UserTripResponse)
def plan_trip(payload: schemas.UserTripCreate, db: Session = Depends(get_db)):
    service = TripsService()
    try:
        trip = service.plan_trip(db, payload)
        return trip
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# List all planned trips for a user
@router.get("/planned", response_model=schemas.UserTripListResponse)
def list_user_trips(email: str, db: Session = Depends(get_db)):
    service = TripsService()
    trips = service.list_user_trips(db, email)
    return {"trips": trips}

# Remove a planned trip for a user
@router.delete("/plan")
def remove_user_trip(email: str, trip_id: int, db: Session = Depends(get_db)):
    service = TripsService()
    try:
        service.remove_user_trip(db, email, trip_id)
        return {"message": "Trip removed"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))