import json
from pathlib import Path
from typing import Optional, List

BASE = Path(__file__).resolve().parents[1] / "data" / "packages"

def _load(name: str):
    with open(BASE / name, encoding="utf-8") as f:
        return json.load(f)

def _apply_filters(items, package_type, price_min, price_max, rating_min):
    if package_type:
        items = [i for i in items if i.get("package_type", "").lower() in {t.lower() for t in package_type}]
    if price_min is not None:
        items = [i for i in items if i.get("price", {}).get("amount", 0) >= price_min]
    if price_max is not None:
        items = [i for i in items if i.get("price", {}).get("amount", 0) <= price_max]
    if rating_min is not None:
        items = [i for i in items if i.get("rating", 0) >= rating_min]
    return items

def _apply_sort(items, sort_by):
    if sort_by == "price_asc":
        return sorted(items, key=lambda x: x["price"]["amount"])
    if sort_by == "price_desc":
        return sorted(items, key=lambda x: x["price"]["amount"], reverse=True)
    if sort_by == "rating":
        return sorted(items, key=lambda x: x.get("rating", 0), reverse=True)
    if sort_by == "popularity":
        return sorted(items, key=lambda x: x.get("popularity", 0), reverse=True)
    return items

def search_packages(destination, start_date, end_date, package_type, price_min, price_max, rating_min, sort_by):
    data = _load("packages_search.json")
    if destination:
        dest_lower = destination.lower()
        data = [d for d in data if dest_lower in d["destination"].lower()]
    data = _apply_filters(data, package_type, price_min, price_max, rating_min)
    data = _apply_sort(data, sort_by)
    return {"count": len(data), "items": data}

def get_package_details(package_id: int):
    details = _load("package_details.json")
    return next((d for d in details if d["id"] == package_id), {})
