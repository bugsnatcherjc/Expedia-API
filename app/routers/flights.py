from fastapi import APIRouter, Query
from typing import Optional, List
from app.services import flights_service

router = APIRouter(prefix="/flights", tags=["Flights"])

@router.get("/search/round-trip")
async def search_round_trip(
    origin: str = Query(..., description="IATA code, e.g., LHE"),
    destination: str = Query(..., description="IATA code, e.g., LAX"),
    depart: str = Query(..., description="YYYY-MM-DD"),
    returnd: str = Query(..., description="YYYY-MM-DD"),
    passengers: int = Query(1, ge=1),
    seat_class: Optional[str] = Query(None, description="economy|premium_economy|business|first"),

   
    stops: Optional[int] = Query(None, description="0,1,2; 2 means 2+"),
    airline: Optional[str] = Query(None, description="Airline code like AA, QR"),
    price_min: Optional[float] = Query(None),
    price_max: Optional[float] = Query(None),

    
    sort_by: Optional[str] = Query(None, description="price_asc|price_desc|duration|departure_time")
):
    return flights_service.search_round_trip(
        origin, destination, depart, returnd, passengers, seat_class,
        stops, airline, price_min, price_max, sort_by
    )


@router.get("/search/one-way")
async def search_one_way(
    origin: str,
    destination: str,
    depart: str,
    passengers: int = Query(1, ge=1),
    seat_class: Optional[str] = None,

    stops: Optional[int] = None,
    airline: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    sort_by: Optional[str] = None
):
    return flights_service.search_one_way(
        origin, destination, depart, passengers, seat_class,
        stops, airline, price_min, price_max, sort_by
    )


@router.get("/search/multi-city")
async def search_multi_city(
    passengers: int = Query(1, ge=1),
    seat_class: Optional[str] = None,

    stops: Optional[int] = None,
    airline: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    sort_by: Optional[str] = None
):
    return flights_service.search_multi_city(
        passengers, seat_class, stops, airline, price_min, price_max, sort_by
    )


@router.get("/details/{flight_id}")
async def flight_details(flight_id: int):
    return flights_service.get_flight_details(flight_id)

@router.get("/status/{flight_number}")
async def flight_status(flight_number: str):
    return flights_service.get_flight_status(flight_number.upper())
