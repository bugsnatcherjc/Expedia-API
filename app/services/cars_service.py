import json
from pathlib import Path
from typing import Optional, List

BASE = Path(__file__).resolve().parents[1] / "data" / "cars"

def _load(name: str):
    with open(BASE / name, encoding="utf-8") as f:
        return json.load(f)

def _apply_filters(items, car_type: Optional[List[str]], company: Optional[List[str]],
                   price_min: Optional[float], price_max: Optional[float], seats_min: Optional[int],
                   transmission: Optional[str], fuel_policy: Optional[str],
                   free_cancellation: Optional[bool], airport_hotel_transfer: Optional[bool]):
    out = items

    if car_type:
        set_types = {t.lower() for t in car_type}
        out = [i for i in out if i.get("car_type", "").lower() in set_types]

    if company:
        set_comp = {c.lower() for c in company}
        out = [i for i in out if i.get("company", "").lower() in set_comp]

    if price_min is not None:
        out = [i for i in out if i.get("price", {}).get("total", 0) >= price_min]

    if price_max is not None:
        out = [i for i in out if i.get("price", {}).get("total", 0) <= price_max]

    if seats_min is not None:
        out = [i for i in out if i.get("capacity", {}).get("seats", 0) >= seats_min]

    if transmission:
        out = [i for i in out if i.get("transmission", "").lower() == transmission.lower()]

    if fuel_policy:
        out = [i for i in out if i.get("fuel_policy", "").lower() == fuel_policy.lower()]

    if free_cancellation is not None:
        out = [i for i in out if i.get("free_cancellation") is free_cancellation]

    if airport_hotel_transfer is not None:
        out = [i for i in out if i.get("airport_hotel_transfer") is airport_hotel_transfer]

    return out

def _apply_sort(items, sort_by: Optional[str]):
    if not sort_by:
        return items
    if sort_by == "price_asc":
        return sorted(items, key=lambda x: x["price"]["total"])
    if sort_by == "price_desc":
        return sorted(items, key=lambda x: x["price"]["total"], reverse=True)
    if sort_by == "rating":
        return sorted(items, key=lambda x: x.get("rating", 0), reverse=True)
    if sort_by == "popularity":
        return sorted(items, key=lambda x: x.get("popularity", 0), reverse=True)
    return items

def search_cars(pickup_location: Optional[str], dropoff_location: Optional[str],
                pickup_datetime: Optional[str], dropoff_datetime: Optional[str],
                airport_hotel_transfer: Optional[bool],
                car_type: Optional[List[str]], company: Optional[List[str]],
                price_min: Optional[float], price_max: Optional[float], seats_min: Optional[int],
                transmission: Optional[str], fuel_policy: Optional[str], free_cancellation: Optional[bool],
                sort_by: Optional[str]):
    data = _load("cars_search.json")

    # Basic location filter: match city or airport code in pickup
    if pickup_location:
        pl = pickup_location.lower()
        data = [d for d in data if pl in d["pickup"]["city"].lower() or pl == d["pickup"].get("airport_code", "").lower()]

    # Optional dropoff filtering (only if provided)
    if dropoff_location:
        dl = dropoff_location.lower()
        data = [d for d in data if dl in d["dropoff"]["city"].lower() or dl == d["dropoff"].get("airport_code", "").lower()]

    data = _apply_filters(
        data, car_type, company, price_min, price_max, seats_min, transmission,
        fuel_policy, free_cancellation, airport_hotel_transfer
    )

    data = _apply_sort(data, sort_by)

    return {"count": len(data), "items": data}

def get_car_details(rental_id: int):
    details = _load("car_details.json")
    # Compare as strings to be robust against int vs str IDs
    return next((d for d in details if str(d["id"]) == str(rental_id)), {})
