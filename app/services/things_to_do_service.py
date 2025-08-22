import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

BASE = Path(__file__).resolve().parents[1] / "data" / "things_to_do"

def _load(name: str):
    with open(BASE / name, encoding="utf-8") as f:
        return json.load(f)

def _get_activity_image(activity_id: str, activity_name: str, category: str) -> str:
    """
    Get appropriate Unsplash image URL based on activity details.
    """
    # Unsplash image URLs for each activity
    image_mapping = {
        "ttd-1": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=800&h=600&fit=crop",  # Universal Studios
        "ttd-2": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=800&h=600&fit=crop",  # Louvre Museum
        "ttd-3": "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&h=600&fit=crop",  # Food Tour
        "ttd-4": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop",  # Grand Canyon
        "ttd-5": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=800&h=600&fit=crop",  # Disney World
    }
    
    return image_mapping.get(activity_id, "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&h=600&fit=crop")

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
    activities = data["activities"]
    for activity in activities:
        if activity["id"] == thing_id:
            return activity
    return None

def get_things_to_do_by_category(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get activities organized by category with optional filtering.
    
    Args:
        category: Optional category filter. If None, returns all categories.
    
    Returns:
        List of category objects with their respective activities.
    """
    data = _load("things_to_do_search.json")
    activities = data["things_to_do"]
    
    # Filter by category if specified
    if category:
        activities = [a for a in activities if a["category"].lower() == category.lower()]
        if not activities:
            return []
    
    # Group activities by category
    category_groups = {}
    for activity in activities:
        cat = activity["category"]
        if cat not in category_groups:
            category_groups[cat] = []
        
        # Transform activity to match the required format
        transformed_activity = {
            "id": int(activity["id"].split("-")[1]),  # Convert ttd-1 to 1
            "title": activity["name"],
            "rating": activity["rating"],
            "reviewsCount": activity["reviews_count"],
            "duration": activity["duration"],
            "price": activity["price"],
            "originalPrice": None,  # Not available in current data
            "currency": "USD",
            "imageUrl": _get_activity_image(activity["id"], activity["name"], activity["category"]),
            "tags": ["Free cancellation"],  # Default tag
            "memberPrice": False  # Default value
        }
        
        category_groups[cat].append(transformed_activity)
    
    # Convert to the required response format
    result = []
    for cat, items in category_groups.items():
        result.append({
            "category": cat,
            "items": items
        })
    
    return result
