from fastapi import APIRouter, Depends
from app.services.stays_service import StaysService

router = APIRouter(prefix="/stays", tags=["Stays"])

@router.get("/")
async def get_stays(service: StaysService = Depends()):
    return service.get_stays()