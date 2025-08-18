from fastapi import APIRouter, Query
from typing import Optional, List
from app.services import stays_service

router = APIRouter(prefix="/stays", tags=["Stays"])

@router.get("/search")
async def search_stays(
    location: Optional[str] = Query(None),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    rating: Optional[float] = Query(None),
    stars: Optional[int] = Query(None),
    amenities: Optional[List[str]] = Query(None),
    sort_by: Optional[str] = Query(None)
):
    return stays_service.search_stays(location, price_min, price_max, rating, stars, amenities, sort_by)

@router.get("/details/{stay_id}")
async def stay_details(stay_id: str):
    return stays_service.get_stay_details(stay_id)

@router.get("/reviews/{stay_id}")
async def stay_reviews(stay_id: str):
    return stays_service.get_stay_reviews(stay_id)

@router.get("/nearby/{stay_id}")
async def nearby_places(stay_id: str):
    return stays_service.get_nearby_places(stay_id)

@router.get("/availability/{stay_id}")
async def stay_availability(stay_id: str):
    return stays_service.get_stay_availability(stay_id)
