from fastapi import APIRouter, Query
from typing import Optional, List
from app.services import cars_service

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.get("/search")
async def search_cars(
    pickup_location: Optional[str] = Query(None, description="city or airport code (e.g., LAX)"),
    dropoff_location: Optional[str] = Query(None),
    pickup_datetime: Optional[str] = Query(None, description="YYYY-MM-DDTHH:MM"),
    dropoff_datetime: Optional[str] = Query(None, description="YYYY-MM-DDTHH:MM"),
    airport_hotel_transfer: Optional[bool] = Query(None, description="true if airport↔hotel transfer"),

    # Filters
    car_type: Optional[List[str]] = Query(None, description="e.g., economy, suv, luxury"),
    company: Optional[List[str]] = Query(None, description="rental company names"),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),
    seats_min: Optional[int] = Query(None),
    transmission: Optional[str] = Query(None, description="automatic|manual"),
    fuel_policy: Optional[str] = Query(None, description="full_to_full|prepurchase"),
    free_cancellation: Optional[bool] = Query(None),

    # Sorting
    sort_by: Optional[str] = Query(None, description="price_asc|price_desc|rating|popularity")
):
    return cars_service.search_cars(
        pickup_location, dropoff_location, pickup_datetime, dropoff_datetime, airport_hotel_transfer,
        car_type, company, price_min, price_max, seats_min, transmission, fuel_policy, free_cancellation,
        sort_by
    )

@router.get("/details/{rental_id}")
async def car_details(rental_id: int):
    return cars_service.get_car_details(rental_id)
