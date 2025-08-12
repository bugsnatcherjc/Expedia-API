from fastapi import APIRouter, Depends
from app.services.trips_service import TripsService

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.get("/")
async def get_trips(service: TripsService = Depends()):
    return service.get_trips()