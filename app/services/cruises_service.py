import json
from pathlib import Path
from typing import Optional
from datetime import datetime

BASE = Path(__file__).resolve().parents[1] / "data" / "cruises"

def _load(name: str):
    with open(BASE / name, encoding="utf-8") as f:
        return json.load(f)

def _apply_filters(results, cruise_line: Optional[str], nights: Optional[int],
                  destination: Optional[str], price_min: Optional[float],
                  price_max: Optional[float], departure_port: Optional[str]):
    out = results

    if cruise_line:
        out = [r for r in out if r["cruise_line"].lower() == cruise_line.lower()]
    
    if nights:
        out = [r for r in out if r["nights"] == nights]
    
    if destination:
        out = [r for r in out if destination.lower() in r["destination"].lower()]
    
    if departure_port:
        out = [r for r in out if departure_port.lower() in r["departure_port"].lower()]
    
    if price_min is not None:
        out = [r for r in out if r["price"] >= price_min]
    
    if price_max is not None:
        out = [r for r in out if r["price"] <= price_max]
    
    return out

def search_cruises(departure_date: str, cruise_line: Optional[str] = None,
                  nights: Optional[int] = None, destination: Optional[str] = None,
                  price_min: Optional[float] = None, price_max: Optional[float] = None,
                  departure_port: Optional[str] = None):
    data = _load("cruises_search.json")
    results = data["cruises"]
    
    # Filter by departure date
    results = [r for r in results if r["departure_date"] >= departure_date]
    
    return _apply_filters(
        results, cruise_line, nights, destination,
        price_min, price_max, departure_port
    )

def get_cruise_details(cruise_id: str):
    data = _load("cruise_details.json")
    return data["cruise_details"] if data["cruise_details"]["id"] == cruise_id else None
