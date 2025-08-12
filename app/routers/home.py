from fastapi import APIRouter, Depends
from app.services.home_service import HomeService
from app.core.deps import get_home_service

router = APIRouter(prefix="/home", tags=["Home"])

@router.get("/navbar")
async def get_navbar(service: HomeService = Depends(get_home_service)):
    return service.get_navbar()