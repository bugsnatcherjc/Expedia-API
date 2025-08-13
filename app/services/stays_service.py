import json
from pathlib import Path
from typing import Optional, List

BASE = Path(__file__).resolve().parents[1] / "data" / "stays"

def load_json(filename: str):
    path = BASE / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def search_stays(location: Optional[str], price_min: Optional[float], price_max: Optional[float],
                 rating: Optional[float], stars: Optional[int], amenities: Optional[List[str]],
                 sort_by: Optional[str]):
    stays = load_json("stays_search.json")

    # Filters
    if location:
        stays = [s for s in stays if location.lower() in s["location"].lower()]
    if price_min is not None:
        stays = [s for s in stays if s["price"] >= price_min]
    if price_max is not None:
        stays = [s for s in stays if s["price"] <= price_max]
    if rating is not None:
        stays = [s for s in stays if s["rating"] >= rating]
    if stars is not None:
        stays = [s for s in stays if s["stars"] == stars]
    if amenities:
        stays = [s for s in stays if all(a in s["amenities"] for a in amenities)]

    # Sorting
    if sort_by == "price_asc":
        stays.sort(key=lambda x: x["price"])
    elif sort_by == "price_desc":
        stays.sort(key=lambda x: x["price"], reverse=True)
    elif sort_by == "rating":
        stays.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == "popularity":
        stays.sort(key=lambda x: x["reviews_count"], reverse=True)

    return stays

def get_stay_details(stay_id: int):
    details = load_json("stays_details.json")
    return next((s for s in details if s["id"] == stay_id), {})

def get_stay_reviews(stay_id: int):
    reviews = load_json("stays_reviews.json")
    return [r for r in reviews if r["stay_id"] == stay_id]

def get_nearby_places(stay_id: int):
    nearby = load_json("stays_nearby.json")
    return [n for n in nearby if n["stay_id"] == stay_id]

def get_stay_availability(stay_id: int):
    availability = load_json("stays_availability.json")
    return next((a for a in availability if a["stay_id"] == stay_id), {})
