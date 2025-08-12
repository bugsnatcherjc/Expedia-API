from fastapi import APIRouter, Depends
from app.services.activities_service import ActivitiesService

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.get("/")
async def get_activities(service: ActivitiesService = Depends()):
    return service.get_activities()
