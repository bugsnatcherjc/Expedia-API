from fastapi import APIRouter, Query
from typing import Optional
from app.services import cruises_service

router = APIRouter(prefix="/cruises", tags=["Cruises"])

@router.get("/search")
async def search_cruises(
    departure_date: str = Query(..., description="YYYY-MM-DD"),
    cruise_line: Optional[str] = Query(None, description="e.g., Royal Caribbean, Carnival"),
    nights: Optional[int] = Query(None, description="Duration in nights"),
    destination: Optional[str] = Query(None, description="e.g., Caribbean, Mediterranean"),
    departure_port: Optional[str] = Query(None, description="e.g., Miami, Barcelona"),
    price_min: Optional[float] = Query(None, description="Minimum price"),
    price_max: Optional[float] = Query(None, description="Maximum price")
):
    """
    Search for available cruises based on various criteria
    """
    return cruises_service.search_cruises(
        departure_date=departure_date,
        cruise_line=cruise_line,
        nights=nights,
        destination=destination,
        departure_port=departure_port,
        price_min=price_min,
        price_max=price_max
    )

@router.get("/{cruise_id}")
async def get_cruise_details(cruise_id: str):
    """
    Get detailed information about a specific cruise
    """
    return cruises_service.get_cruise_details(cruise_id)
