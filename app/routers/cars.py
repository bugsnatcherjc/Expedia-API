from fastapi import APIRouter, Depends
from app.services.cars_service import CarsService

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.get("/")
async def get_cars(service: CarsService = Depends()):
    return service.get_cars()