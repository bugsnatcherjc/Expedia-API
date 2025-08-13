from fastapi import APIRouter, Query
from typing import Optional, List
from app.services import activities_service

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.get("/search")
async def search_activities(
    location: Optional[str] = Query(None, description="City or country"),
    date: Optional[str] = Query(None, description="YYYY-MM-DD"),

    # Filters
    category: Optional[List[str]] = Query(None, description="e.g., adventure, cultural"),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    rating_min: Optional[float] = Query(None),

    # Sorting
    sort_by: Optional[str] = Query(None, description="price_asc|price_desc|rating|popularity")
):
    return activities_service.search_activities(
        location, date, category, price_min, price_max, rating_min, sort_by
    )

@router.get("/details/{activity_id}")
async def activity_details(activity_id: int):
    return activities_service.get_activity_details(activity_id)
