import json
from pathlib import Path
from typing import Optional
from datetime import datetime

BASE = Path(__file__).resolve().parents[1] / "data" / "things_to_do"

def _load(name: str):
    with open(BASE / name, encoding="utf-8") as f:
        return json.load(f)

def _apply_filters(results, category: Optional[str], price_min: Optional[float],
                  price_max: Optional[float], duration: Optional[str],
                  min_rating: Optional[float]):
    out = results

    if category:
        out = [r for r in out if r["category"].lower() == category.lower()]
    
    if duration:
        out = [r for r in out if r["duration"].lower() == duration.lower()]
    
    if min_rating is not None:
        out = [r for r in out if r["rating"] >= min_rating]
    
    if price_min is not None:
        out = [r for r in out if r["price"] >= price_min]
    
    if price_max is not None:
        out = [r for r in out if r["price"] <= price_max]
    
    return out

def search_things_to_do(location: str, date: str, category: Optional[str] = None,
                       price_min: Optional[float] = None, price_max: Optional[float] = None,
                       duration: Optional[str] = None, min_rating: Optional[float] = None):
    data = _load("things_to_do_search.json")
    results = data["things_to_do"]
    
    # Filter by location and date
    results = [r for r in results 
              if location.lower() in r["location"].lower() 
              and date in r["available_dates"]]
    
    return _apply_filters(
        results, category, price_min, price_max,
        duration, min_rating
    )

def get_thing_details(thing_id: str):
    data = _load("thing_details.json")
    return data["activity_details"] if data["activity_details"]["id"] == thing_id else None
