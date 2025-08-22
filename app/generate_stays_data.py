import argparse
import json
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "stays"
META_DIR = ROOT / "data" / "meta-ui"


# Domain enums and helpers
STAR_RATINGS = [3, 4, 5]
CURRENCIES = ["USD", "EUR", "GBP", "JPY", "AED", "SGD"]
HOTEL_CHAINS = [
    "Marriott", "Hilton", "Hyatt", "InterContinental", "Four Seasons", "Ritz-Carlton",
    "W Hotels", "Sheraton", "Westin", "Renaissance", "Courtyard", "Residence Inn"
]
INDEPENDENT_HOTELS = [
    "The Plaza", "Waldorf Astoria", "The Peninsula", "Mandarin Oriental", "Aman Resorts",
    "Banyan Tree", "Six Senses", "Rosewood", "Belmond", "Oberoi"
]


@dataclass
class Location:
    id: str
    city: str
    area: str
    state: str
    country: str
    lat: float
    lng: float
    airports: List[str]
    popular_areas: List[str]
    type: List[str]


@dataclass
class Amenity:
    name: str
    category: str


def load_locations() -> List[Location]:
    with open(META_DIR / "stays_locations.json", encoding="utf-8") as f:
        items = json.load(f)
    out: List[Location] = []
    for i in items:
        out.append(
            Location(
                id=i["id"],
                city=i["city"],
                area=i["area"],
                state=i["state"],
                country=i["country"],
                lat=float(i.get("lat") or 0),
                lng=float(i.get("lng") or 0),
                airports=i.get("airports", []),
                popular_areas=i.get("popular_areas", []),
                type=i.get("type", [])
            )
        )
    return out


def load_amenities() -> List[Amenity]:
    with open(META_DIR / "stays_amenities.json", encoding="utf-8") as f:
        data = json.load(f)
    amenities = []
    for category in data["categories"]:
        for amenity_name in category["amenities"]:
            amenities.append(Amenity(name=amenity_name, category=category["name"]))
    return amenities


def seeded_random(seed: str) -> random.Random:
    rnd = random.Random()
    rnd.seed(seed)
    return rnd


def generate_hotel_name(rnd: random.Random, location: Location, stars: int) -> str:
    """Generate realistic hotel names based on location and star rating"""
    
    # Luxury hotel names for 5-star properties
    if stars == 5:
        luxury_prefixes = ["The", "Grand", "Royal", "Imperial", "Palace"]
        luxury_suffixes = ["Hotel", "Resort", "Tower", "Plaza", "Manor"]
        
        if rnd.random() < 0.7:  # 70% chance for chain hotel
            chain = rnd.choice(HOTEL_CHAINS)
            suffix = rnd.choice(luxury_suffixes)
            return f"{chain} {location.city} {suffix}"
        else:
            prefix = rnd.choice(luxury_prefixes)
            suffix = rnd.choice(luxury_suffixes)
            return f"{prefix} {location.city} {suffix}"
    
    # Standard hotel names for 3-4 star properties
    else:
        standard_prefixes = ["", "Best Western", "Comfort Inn", "Holiday Inn", "Quality Inn"]
        standard_suffixes = ["Hotel", "Inn", "Suites", "Lodge"]
        
        if rnd.random() < 0.8:  # 80% chance for chain hotel
            chain = rnd.choice(standard_prefixes)
            if chain:
                return f"{chain} {location.city}"
            else:
                suffix = rnd.choice(standard_suffixes)
                return f"{location.city} {suffix}"
        else:
            suffix = rnd.choice(standard_suffixes)
            return f"{location.city} {suffix}"


def generate_hotel_photos(rnd: random.Random, stars: int, location: Location) -> List[str]:
    """Generate realistic hotel photos from Unsplash based on star rating and location type"""
    
    # Base hotel photos by star rating
    base_photos = {
        3: [
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&h=600&fit=crop"
        ],
        4: [
            "https://images.unsplash.com/photo-1602002418816-5c0aeef426aa?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&h=600&fit=crop"
        ],
        5: [
            "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1549294413-26f195f4d04d?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&h=600&fit=crop"
        ]
    }
    
    # Location-specific photos
    location_photos = {
        "Beach": [
            "https://images.unsplash.com/photo-1602002418816-5c0aeef426aa?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?w=800&h=600&fit=crop"
        ],
        "City": [
            "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&h=600&fit=crop"
        ],
        "Mountain": [
            "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=800&h=600&fit=crop",
            "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&h=600&fit=crop"
        ]
    }
    
    photos = base_photos[stars].copy()
    
    # Add location-specific photos if available
    for loc_type in location.type:
        if loc_type in location_photos:
            photos.extend(location_photos[loc_type])
    
    # Select appropriate number of photos based on star rating
    num_photos = min(rnd.randint(stars + 2, stars + 4), len(photos))
    return rnd.sample(photos, num_photos)


def generate_room_photos(rnd: random.Random, room_type: str) -> List[str]:
    """Generate room photos from Unsplash"""
    room_photos = [
        "https://images.unsplash.com/photo-1591088398332-8a7791972843?w=800&h=600&fit=crop",
        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop",
        "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&h=600&fit=crop",
        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop",
        "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&h=600&fit=crop"
    ]
    return rnd.sample(room_photos, rnd.randint(1, 3))


def generate_price(rnd: random.Random, stars: int, location: Location, currency: str) -> float:
    """Generate realistic hotel prices based on star rating and location"""
    
    # Base prices by star rating (in USD)
    base_prices = {
        3: (80, 150),
        4: (150, 350),
        5: (300, 1200)
    }
    
    min_price, max_price = base_prices[stars]
    
    # Location multipliers
    location_multipliers = {
        "New York": 1.8,
        "Miami Beach": 1.5,
        "San Francisco": 1.6,
        "Paris": 1.4,
        "Dubai": 1.3,
        "Tokyo": 1.7,
        "Las Vegas": 1.2,
        "Singapore": 1.5
    }
    
    multiplier = location_multipliers.get(location.city, 1.0)
    
    # Generate price with some randomness
    base_price = rnd.uniform(min_price, max_price) * multiplier
    
    # Currency conversion (simplified)
    currency_rates = {
        "USD": 1.0,
        "EUR": 0.85,
        "GBP": 0.75,
        "JPY": 110.0,
        "AED": 3.67,
        "SGD": 1.35
    }
    
    usd_price = base_price
    local_price = usd_price / currency_rates.get(currency, 1.0)
    
    return round(local_price, 2)


def generate_amenities(rnd: random.Random, stars: int, location: Location) -> List[str]:
    """Generate realistic amenities based on star rating and location"""
    all_amenities = load_amenities()
    
    # Base amenities that all hotels have
    base_amenities = ["Free WiFi", "Air Conditioning"]
    
    # Star-based amenities
    star_amenities = {
        3: ["24-hour front desk", "Parking", "Flat-screen TV"],
        4: ["Pool", "Gym", "Restaurant", "Bar", "Concierge service"],
        5: ["Spa", "Infinity Pool", "Michelin Restaurant", "Butler Service", "Private Beach"]
    }
    
    # Location-specific amenities
    location_amenities = {
        "Beach": ["Beachfront", "Water Sports", "Private Beach"],
        "Mountain": ["Ski-in/Ski-out", "Mountain View"],
        "City": ["City Views", "Business Center", "Shopping"]
    }
    
    amenities = base_amenities.copy()
    amenities.extend(star_amenities[stars])
    
    # Add location-specific amenities
    for loc_type in location.type:
        if loc_type in location_amenities:
            amenities.extend(location_amenities[loc_type])
    
    # Randomly select additional amenities
    available_amenities = [a.name for a in all_amenities if a.name not in amenities]
    additional_count = rnd.randint(2, 5)
    additional = rnd.sample(available_amenities, min(additional_count, len(available_amenities)))
    
    amenities.extend(additional)
    return amenities


def generate_rooms(rnd: random.Random, hotel_name: str, stars: int, base_price: float, currency: str) -> List[Dict]:
    """Generate room types for a hotel"""
    room_types = {
        3: ["Standard Room", "Deluxe Room", "Suite"],
        4: ["Standard Room", "Deluxe Room", "Executive Suite", "Family Room"],
        5: ["Deluxe Room", "Executive Suite", "Presidential Suite", "Villa", "Penthouse"]
    }
    
    rooms = []
    room_id_counter = 1
    
    for room_type in room_types[stars]:
        # Price variation based on room type
        price_multipliers = {
            "Standard Room": 1.0,
            "Deluxe Room": 1.3,
            "Executive Suite": 1.8,
            "Family Room": 1.5,
            "Presidential Suite": 3.0,
            "Villa": 2.5,
            "Penthouse": 4.0
        }
        
        price = base_price * price_multipliers.get(room_type, 1.0)
        price = round(price * rnd.uniform(0.9, 1.1), 2)
        
        # Bed configuration
        bed_configs = {
            "Standard Room": ["1 Queen Bed", "1 King Bed", "2 Twin Beds"],
            "Deluxe Room": ["1 King Bed", "2 Queen Beds"],
            "Executive Suite": ["1 King Bed", "1 King Bed + Sofa Bed"],
            "Family Room": ["2 Queen Beds", "1 King Bed + 2 Twin Beds"],
            "Presidential Suite": ["1 King Bed", "1 King Bed + Separate Bedroom"],
            "Villa": ["1 King Bed + 2 Twin Beds", "2 King Beds"],
            "Penthouse": ["1 King Bed + Separate Bedroom", "2 King Beds + Study"]
        }
        
        bed_type = rnd.choice(bed_configs.get(room_type, ["1 King Bed"]))
        max_occupancy = min(6, len([b for b in bed_type.split() if "Bed" in b]) * 2)
        
        room = {
            "id": f"room-{room_id_counter:03d}",
            "type": room_type,
            "price_per_night": price,
            "currency": currency,
            "max_occupancy": max_occupancy,
            "bed_type": bed_type,
            "amenities": [
                "Air Conditioning",
                "Mini Bar",
                "Free WiFi",
                "Flat-screen TV",
                "City View" if "City" in room_type else "Garden View"
            ],
            "photos": generate_room_photos(rnd, room_type),
            "cancellation": "Free cancellation until 3 days before check-in",
            "available": rnd.choice([True, True, True, False])  # 75% chance available
        }
        
        rooms.append(room)
        room_id_counter += 1
    
    return rooms


def generate_records(
    days: int,
    max_hotels_per_location: int,
    seed: str,
) -> Tuple[List[Dict], List[Dict], List[Dict], List[Dict], List[Dict]]:
    locations = load_locations()
    
    items_search: List[Dict] = []
    items_details: List[Dict] = []
    items_reviews: List[Dict] = []
    items_nearby: List[Dict] = []
    items_availability: List[Dict] = []
    
    start_date = datetime.utcnow().date()
    id_counter = 10000
    
    for location in locations:
        # Generate 2-4 hotels per location based on city size
        location_rnd = seeded_random(f"{seed}:{location.id}")
        num_hotels = min(max_hotels_per_location, location_rnd.randint(2, 4))
        
        for hotel_idx in range(num_hotels):
            rnd = seeded_random(f"{seed}:{location.id}:{hotel_idx}")
            
            # Generate hotel properties
            stars = rnd.choice(STAR_RATINGS)
            currency = rnd.choice(CURRENCIES)
            hotel_name = generate_hotel_name(rnd, location, stars)
            base_price = generate_price(rnd, stars, location, currency)
            amenities = generate_amenities(rnd, stars, location)
            photos = generate_hotel_photos(rnd, stars, location)
            thumbnail = photos[0] if photos else ""
            
            # Generate hotel ID
            hotel_id = f"stay-{id_counter:03d}"
            id_counter += 1
            
            # Generate description
            descriptions = [
                f"Experience luxury and comfort in the heart of {location.city}. Perfect for both business and leisure travelers.",
                f"A {stars}-star accommodation offering world-class amenities and exceptional service in {location.city}.",
                f"Located in {location.area}, this hotel provides easy access to {', '.join(location.popular_areas[:2])}.",
                f"Discover the perfect blend of comfort and style in {location.city}, featuring modern amenities and stunning views."
            ]
            description = rnd.choice(descriptions)
            
            # Generate cancellation policy
            cancellation_policies = [
                "Free cancellation until 3 days before check-in",
                "Free cancellation until 7 days before check-in",
                "Free cancellation until 14 days before check-in",
                "Non-refundable rate"
            ]
            cancellation_policy = rnd.choice(cancellation_policies)
            is_cancellable = "Non-refundable" not in cancellation_policy
            
            # Generate rating and reviews
            rating = round(rnd.uniform(3.5, 5.0), 1)
            reviews_count = rnd.randint(100, 8000)
            
            # Search item
            search_item = {
                "id": hotel_id,
                "name": hotel_name,
                "location": f"{location.city}, {location.country}",
                "price": base_price,
                "currency": currency,
                "member_price": round(base_price * 0.9, 2),
                "rating": rating,
                "reviews_count": reviews_count,
                "is_cancellable": is_cancellable,
                "cancellation_policy": cancellation_policy,
                "stars": stars,
                "amenities": amenities,
                "thumbnail": thumbnail,
                "coordinates": {"lat": location.lat, "lng": location.lng},
                "description": description,
                "photos": photos
            }
            items_search.append(search_item)
            
            # Details item
            address = f"{rnd.randint(100, 9999)} {location.area} Street, {location.city}, {location.state} {rnd.randint(10000, 99999)}"
            rooms = generate_rooms(rnd, hotel_name, stars, base_price, currency)
            
            details_item = {
                "id": hotel_id,
                "name": hotel_name,
                "location": f"{location.city}, {location.country}",
                "address": address,
                "description": description,
                "stars": stars,
                "rating": rating,
                "reviews_count": reviews_count,
                "coordinates": {"lat": location.lat, "lng": location.lng},
                "is_cancellable": is_cancellable,
                "cancellation_policy": cancellation_policy,
                "thumbnail": thumbnail,
                "photos": photos,
                "rooms": rooms,
                "price": base_price,
                "currency": currency,
                "member_price": round(base_price * 0.9, 2)
            }
            items_details.append(details_item)
            
            # Reviews
            num_reviews = min(10, reviews_count // 100)
            for review_idx in range(num_reviews):
                review_rnd = seeded_random(f"{seed}:{hotel_id}:review:{review_idx}")
                review_date = start_date - timedelta(days=review_rnd.randint(1, 365))
                
                review = {
                    "id": f"review-{id_counter:06d}",
                    "stay_id": hotel_id,
                    "user_name": f"Guest{review_rnd.randint(1000, 9999)}",
                    "rating": review_rnd.randint(1, 5),
                    "comment": "Great stay, highly recommended!",
                    "date": review_date.isoformat(),
                    "helpful_votes": review_rnd.randint(0, 20)
                }
                items_reviews.append(review)
                id_counter += 1
            
            # Nearby places
            num_nearby = rnd.randint(3, 8)
            for nearby_idx in range(num_nearby):
                nearby_rnd = seeded_random(f"{seed}:{hotel_id}:nearby:{nearby_idx}")
                nearby_types = ["Restaurant", "Shopping", "Attraction", "Transport", "Entertainment"]
                
                nearby = {
                    "id": f"nearby-{id_counter:06d}",
                    "stay_id": hotel_id,
                    "name": f"{nearby_rnd.choice(nearby_types)} {nearby_rnd.randint(1, 100)}",
                    "type": nearby_rnd.choice(nearby_types),
                    "distance": round(nearby_rnd.uniform(0.1, 2.0), 1),
                    "rating": round(nearby_rnd.uniform(3.0, 5.0), 1)
                }
                items_nearby.append(nearby)
                id_counter += 1
            
            # Availability for next 30 days
            for day_offset in range(days):
                avail_rnd = seeded_random(f"{seed}:{hotel_id}:availability:{day_offset}")
                check_in = start_date + timedelta(days=day_offset)
                check_out = check_in + timedelta(days=rnd.randint(1, 7))
                
                # Generate room availability
                room_availability = []
                for room in rooms:
                    room_avail = {
                        "room_id": room["id"],
                        "available": avail_rnd.choice([True, True, True, False]),  # 75% chance
                        "price_per_night": room["price_per_night"],
                        "currency": room["currency"]
                    }
                    room_availability.append(room_avail)
                
                availability = {
                    "id": f"avail-{id_counter:06d}",
                    "stay_id": hotel_id,
                    "check_in": check_in.isoformat(),
                    "check_out": check_out.isoformat(),
                    "rooms": room_availability
                }
                items_availability.append(availability)
                id_counter += 1
    
    return items_search, items_details, items_reviews, items_nearby, items_availability


def write_files(search_items: List[Dict], detail_items: List[Dict], review_items: List[Dict], 
                nearby_items: List[Dict], availability_items: List[Dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Write search file
    with open(DATA_DIR / "stays_search.json", "w", encoding="utf-8") as f:
        json.dump({"stays": search_items}, f, ensure_ascii=False, indent=2)
    
    # Write details file
    with open(DATA_DIR / "stays_details.json", "w", encoding="utf-8") as f:
        json.dump({"stays": detail_items}, f, ensure_ascii=False, indent=2)
    
    # Write reviews file
    with open(DATA_DIR / "stays_reviews.json", "w", encoding="utf-8") as f:
        json.dump(review_items, f, ensure_ascii=False, indent=2)
    
    # Write nearby file
    with open(DATA_DIR / "stays_nearby.json", "w", encoding="utf-8") as f:
        json.dump(nearby_items, f, ensure_ascii=False, indent=2)
    
    # Write availability file
    with open(DATA_DIR / "stays_availability.json", "w", encoding="utf-8") as f:
        json.dump(availability_items, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Generate stays search and detail data")
    parser.add_argument("--days", type=int, default=30, help="Number of future days to generate availability for")
    parser.add_argument("--max-hotels-per-location", type=int, default=3, help="Maximum hotels to generate per location")
    parser.add_argument("--seed", type=str, default="stays", help="Deterministic seed base")

    args = parser.parse_args()
    
    search_items, detail_items, review_items, nearby_items, availability_items = generate_records(
        days=args.days,
        max_hotels_per_location=args.max_hotels_per_location,
        seed=args.seed,
    )
    
    write_files(search_items, detail_items, review_items, nearby_items, availability_items)
    
    print(
        f"Generated {len(search_items)} search items, {len(detail_items)} detail items, "
        f"{len(review_items)} reviews, {len(nearby_items)} nearby places, and "
        f"{len(availability_items)} availability records for {args.days} day(s)."
    )


if __name__ == "__main__":
    main()
