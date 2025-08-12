from fastapi import APIRouter, Depends
from app.services.flights_service import FlightsService

router = APIRouter(prefix="/flights", tags=["Flights"])

@router.get("/")
async def get_flights(service: FlightsService = Depends()):
    return service.get_flights()