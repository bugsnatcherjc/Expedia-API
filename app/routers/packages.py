from fastapi import APIRouter, Query
from typing import Optional, List
from app.services import packages_service

router = APIRouter(prefix="/packages", tags=["Packages"])

@router.get("/search")
async def search_packages(
    destination: Optional[str] = Query(None, description="City or country"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),

    # Filters
    package_type: Optional[List[str]] = Query(None, description="e.g., honeymoon, family"),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    rating_min: Optional[float] = Query(None),

    # Sorting
    sort_by: Optional[str] = Query(None, description="price_asc|price_desc|rating|popularity")
):
    return packages_service.search_packages(
        destination, start_date, end_date, package_type, price_min, price_max, rating_min, sort_by
    )

@router.get("/details/{package_id}")
async def package_details(package_id: int):
    return packages_service.get_package_details(package_id)
