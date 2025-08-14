from fastapi import APIRouter, Query
from typing import Optional
from app.services import things_to_do_service

router = APIRouter(prefix="/things-to-do", tags=["Things To Do"])

@router.get("/search")
async def search_things_to_do(
    location: str = Query(..., description="City, State or Area"),
    date: str = Query(..., description="YYYY-MM-DD"),
    category: Optional[str] = Query(None, description="e.g., Theme Parks, Tours, Museums"),
    duration: Optional[str] = Query(None, description="e.g., 1 day, 2 hours"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating (0-5)"),
    price_min: Optional[float] = Query(None, description="Minimum price"),
    price_max: Optional[float] = Query(None, description="Maximum price")
):
    """
    Search for things to do in a specific location
    """
    return things_to_do_service.search_things_to_do(
        location=location,
        date=date,
        category=category,
        duration=duration,
        min_rating=min_rating,
        price_min=price_min,
        price_max=price_max
    )

@router.get("/{thing_id}")
async def get_thing_details(thing_id: str):
    """
    Get detailed information about a specific activity or attraction
    """
    return things_to_do_service.get_thing_details(thing_id)
