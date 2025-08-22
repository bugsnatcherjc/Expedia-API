import argparse
import json
import math
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "cars"
META_DIR = ROOT / "data" / "meta-ui"


# Domain enums and helpers
CAR_TYPES = [
    "mini", "economy", "compact", "midsize", "standard", "fullsize",
    "premium", "luxury", "suv", "convertible", "sports", "van"
]
TRANSMISSIONS = ["automatic", "manual"]
FUEL_POLICIES = ["full_to_full", "prepurchase"]
CURRENCIES = ["USD", "EUR", "GBP"]


@dataclass
class Location:
    id: str
    city: str
    country: str
    airport_code: Optional[str]
    lat: float
    lng: float


@dataclass
class Brand:
    name: str
    logo: str


def load_locations() -> List[Location]:
    with open(META_DIR / "car_locations.json", encoding="utf-8") as f:
        items = json.load(f)
    out: List[Location] = []
    for i in items:
        out.append(
            Location(
                id=i["id"],
                city=i["city"],
                country=i["country"],
                airport_code=i.get("airport_code"),
                lat=float(i.get("lat") or 0),
                lng=float(i.get("lng") or 0),
            )
        )
    return out


def load_brands() -> List[Brand]:
    with open(META_DIR / "car_brands.json", encoding="utf-8") as f:
        items = json.load(f)
    return [Brand(name=i["name"], logo=i["logo"]) for i in items]


def seeded_random(seed: str) -> random.Random:
    rnd = random.Random()
    rnd.seed(seed)
    return rnd


def pick_company_logo(brand: Brand) -> Tuple[str, str]:
    return brand.name, brand.logo


def generate_car_photos(rnd: random.Random, car_type: str, brand: str) -> List[str]:
    """Generate realistic car photos from Unsplash based on car type and brand"""
    
    # Base Unsplash car photos by type
    type_photos = {
        "mini": [
            "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=640&h=360&fit=crop"
        ],
        "economy": [
            "https://images.unsplash.com/photo-1590362891991-f776e747a588?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1471444928139-48c5bf5173f8?w=640&h=360&fit=crop"
        ],
        "compact": [
            "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1471444928139-48c5bf5173f8?w=640&h=360&fit=crop"
        ],
        "midsize": [
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop"
        ],
        "standard": [
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1581465706166-4bf9c2a02c16?w=640&h=360&fit=crop"
        ],
        "fullsize": [
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1581465706166-4bf9c2a02c16?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=640&h=360&fit=crop"
        ],
        "premium": [
            "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1581465706166-4bf9c2a02c16?w=640&h=360&fit=crop"
        ],
        "luxury": [
            "https://images.unsplash.com/photo-1523983388277-336a66bf9bcd?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop"
        ],
        "suv": [
            "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1581465706166-4bf9c2a02c16?w=640&h=360&fit=crop"
        ],
        "convertible": [
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop"
        ],
        "sports": [
            "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1523983388277-336a66bf9bcd?w=640&h=360&fit=crop"
        ],
        "van": [
            "https://images.unsplash.com/photo-1581465706166-4bf9c2a02c16?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=640&h=360&fit=crop"
        ]
    }
    
    # Brand-specific photos for premium/luxury cars
    brand_photos = {
        "BMW": [
            "https://images.unsplash.com/photo-1523983388277-336a66bf9bcd?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1581465706166-4bf9c2a02c16?w=640&h=360&fit=crop"
        ],
        "Mercedes-Benz": [
            "https://images.unsplash.com/photo-1563720360172-67b8f3dce741?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1581465706166-4bf9c2a02c16?w=640&h=360&fit=crop"
        ],
        "Audi": [
            "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1581465706166-4bf9c2a02c16?w=640&h=360&fit=crop"
        ],
        "Toyota": [
            "https://images.unsplash.com/photo-1590362891991-f776e747a588?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1581465706166-4bf9c2a02c16?w=640&h=360&fit=crop"
        ],
        "Honda": [
            "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1589974725932-171b6cb613ec?w=640&h=360&fit=crop",
            "https://images.unsplash.com/photo-1581465706166-4bf9c2a02c16?w=640&h=360&fit=crop"
        ]
    }
    
    # Get base photos for car type
    base_photos = type_photos.get(car_type, type_photos["economy"])
    
    # For premium/luxury cars, mix with brand-specific photos
    if car_type in ["premium", "luxury"] and brand in brand_photos:
        all_photos = base_photos + brand_photos[brand]
        # Select 3-4 photos, prioritizing brand photos
        num_photos = rnd.randint(3, 4)
        if num_photos <= len(brand_photos[brand]):
            return rnd.sample(brand_photos[brand], num_photos)
        else:
            selected = rnd.sample(brand_photos[brand], len(brand_photos[brand]))
            remaining = rnd.sample(base_photos, num_photos - len(brand_photos[brand]))
            return selected + remaining
    
    # For regular cars, select 2-3 photos from base type
    num_photos = rnd.randint(2, 3)
    return rnd.sample(base_photos, num_photos)


def generate_price(rnd: random.Random, car_type: str, currency: str) -> Dict:
    base = {
        "mini": 28,
        "economy": 32,
        "compact": 36,
        "midsize": 42,
        "standard": 48,
        "fullsize": 55,
        "premium": 75,
        "luxury": 110,
        "suv": 70,
        "convertible": 95,
        "sports": 90,
        "van": 65,
    }.get(car_type, 50)

    day_rate = base * rnd.uniform(0.85, 1.25)
    day_rate = round(day_rate, 1)
    return {"per_day": day_rate, "currency": currency}


def generate_capacity(rnd: random.Random, car_type: str) -> Dict:
    seats = {
        "mini": 4,
        "economy": 5,
        "compact": 5,
        "midsize": 5,
        "standard": 5,
        "fullsize": 5,
        "premium": 5,
        "luxury": 5,
        "suv": 7,
        "convertible": 4,
        "sports": 4,
        "van": 8,
    }.get(car_type, 5)
    bags = max(1, math.floor(seats / 2))
    if car_type in ("suv", "van"):
        bags += 1
    return {"seats": seats, "bags": bags}


def make_model(brand: str, car_type: str, rnd: random.Random) -> str:
    examples = {
        "Toyota": {
            "economy": ["Yaris", "Corolla"],
            "suv": ["RAV4", "Highlander"],
            "compact": ["Corolla"],
            "midsize": ["Camry"],
            "van": ["Sienna"],
        },
        "Honda": {"economy": ["Fit"], "compact": ["Civic"], "suv": ["CR-V"], "midsize": ["Accord"]},
        "BMW": {"luxury": ["5 Series", "3 Series"], "sports": ["M4"]},
        "Mercedes-Benz": {"luxury": ["C-Class", "E-Class"], "premium": ["GLC"]},
        "Audi": {"premium": ["A4"], "luxury": ["A6"]},
        "Chevrolet": {"midsize": ["Malibu"], "sports": ["Camaro"], "suv": ["Tahoe"]},
        "Volkswagen": {"economy": ["Polo"], "compact": ["Golf"]},
        "Hyundai": {"midsize": ["Sonata"], "compact": ["i30"]},
        "Peugeot": {"compact": ["308"], "economy": ["208"]},
        "Ford": {"midsize": ["Fusion"], "sports": ["Mustang"], "suv": ["Explorer"]},
    }
    opts = examples.get(brand, {}).get(car_type, [car_type.title()])
    return f"{brand} {rnd.choice(opts)}"


def generate_records(
    days: int,
    full_combinations: bool,
    max_per_combo: int,
    seed: str,
) -> Tuple[List[Dict], List[Dict]]:
    locations = load_locations()
    brands = load_brands()

    items_search: List[Dict] = []
    items_details: List[Dict] = []

    start_date = datetime.utcnow().date()
    id_counter = 10000

    # Build combinations
    locations_pairs: List[Tuple[Location, Location]] = []
    for pick in locations:
        for drop in locations:
            if not full_combinations and drop.id != pick.id:
                continue
            locations_pairs.append((pick, drop))

    for day_offset in range(days):
        pickup_dt = datetime.combine(start_date + timedelta(days=day_offset), datetime.min.time()).replace(hour=10)
        dropoff_dt = pickup_dt + timedelta(days=1)
        for pick, drop in locations_pairs:
            # For each car_type and transmission combinations
            for car_type in CAR_TYPES:
                for transmission in TRANSMISSIONS:
                    # Sample a subset of brands to limit size if required
                    rnd = seeded_random(f"{seed}:{day_offset}:{pick.id}:{drop.id}:{car_type}:{transmission}")
                    selected_brands = brands if full_combinations else rnd.sample(brands, k=min(3, len(brands)))

                    # Iterate free_cancellation, airport_hotel_transfer, fuel_policy
                    bool_pairs = [(False, False), (True, False), (False, True), (True, True)]
                    for free_cancellation, airport_hotel_transfer in bool_pairs:
                        for fuel_policy in FUEL_POLICIES:
                            currency = rnd.choice(CURRENCIES)
                            combo_count = 0
                            for brand in selected_brands:
                                if not full_combinations and combo_count >= max_per_combo:
                                    break

                                company, logo = pick_company_logo(brand)
                                capacity = generate_capacity(rnd, car_type)
                                price_per_day = generate_price(rnd, car_type, currency)
                                total_days = max(1, (dropoff_dt - pickup_dt).days)
                                total_price = round(price_per_day["per_day"] * total_days, 1)
                                rating = round(rnd.uniform(3.9, 4.9), 1)
                                popularity = rnd.randint(100, 1200)
                                year = rnd.choice([2020, 2021, 2022, 2023, 2024])
                                fuel = rnd.choice(["petrol", "diesel", "hybrid"]) if car_type not in ("sports",) else "petrol"

                                car_model = make_model(company, car_type, rnd)
                                
                                # Generate photos
                                photos = generate_car_photos(rnd, car_type, company)

                                # IDs
                                id_counter += 1
                                rental_id = id_counter

                                # Search item
                                items_search.append(
                                    {
                                        "id": rental_id,
                                        "company": company,
                                        "company_logo": logo,
                                        "car_model": car_model,
                                        "car_type": car_type,
                                        "transmission": transmission,
                                        "capacity": capacity,
                                        "air_conditioning": True,
                                        "fuel_policy": fuel_policy,
                                        "free_cancellation": free_cancellation,
                                        "airport_hotel_transfer": airport_hotel_transfer,
                                        "price": {
                                            "total": total_price,
                                            "currency": currency,
                                            "per_day": price_per_day["per_day"],
                                        },
                                        "member_price": {
                                            "total": round(total_price * 0.85, 1),
                                            "currency": currency,
                                            "per_day": round(price_per_day["per_day"] * 0.85, 1),
                                        },
                                        "rating": rating,
                                        "popularity": popularity,
                                        "pickup": {
                                            "city": pick.city,
                                            "country": pick.country,
                                            "airport_code": pick.airport_code,
                                            "lat": pick.lat,
                                            "lng": pick.lng,
                                            "datetime": pickup_dt.isoformat(timespec="minutes"),
                                        },
                                        "dropoff": {
                                            "city": drop.city,
                                            "country": drop.country,
                                            "airport_code": drop.airport_code,
                                            "lat": drop.lat,
                                            "lng": drop.lng,
                                            "datetime": dropoff_dt.isoformat(timespec="minutes"),
                                        },
                                        "photos": photos,
                                    }
                                )

                                # Details item
                                items_details.append(
                                    {
                                        "id": rental_id,
                                        "company": company,
                                        "company_logo": logo,
                                        "car_model": car_model,
                                        "year": year,
                                        "car_type": car_type,
                                        "doors": 4 if capacity["seats"] <= 5 else 5,
                                        "transmission": transmission,
                                        "fuel": fuel,
                                        "fuel_policy": fuel_policy,
                                        "air_conditioning": True,
                                        "capacity": capacity,
                                        "included": [
                                            "Collision Damage Waiver",
                                            "Theft Protection",
                                            "Unlimited mileage",
                                        ],
                                        "extras_available": ["GPS", "Child seat", "Additional driver"],
                                        "terms": {
                                            "deposit": f"{currency} {rnd.choice([200, 250, 300, 400])}",
                                            "min_age": rnd.choice([21, 23, 25]),
                                            "drivers_license": "Valid license held for 1+ year",
                                            "cross_border": rnd.choice(["Not allowed", "On request", "Allowed within CA"]),
                                        },
                                        "pickup": {
                                            "address": f"{pick.city} Rental Car Center",
                                            "city": pick.city,
                                            "lat": pick.lat,
                                            "lng": pick.lng,
                                            "datetime": pickup_dt.isoformat(timespec="minutes"),
                                        },
                                        "dropoff": {
                                            "address": f"{drop.city} Rental Car Center",
                                            "city": drop.city,
                                            "lat": drop.lat,
                                            "lng": drop.lng,
                                            "datetime": dropoff_dt.isoformat(timespec="minutes"),
                                        },
                                        "photos": photos,
                                        "price": {
                                            "per_day": price_per_day["per_day"],
                                            "days": total_days,
                                            "total": total_price,
                                            "currency": currency,
                                        },
                                        "member_price": {
                                            "per_day": round(price_per_day["per_day"] * 0.85, 1),
                                            "days": total_days,
                                            "total": round(total_price * 0.85, 1),
                                            "currency": currency,
                                        },
                                        "cancellation_policy": (
                                            "Free cancellation up to 24h before pickup"
                                            if free_cancellation
                                            else "Non-refundable rate"
                                        ),
                                    }
                                )

                                combo_count += 1

    return items_search, items_details


def write_files(search_items: List[Dict], detail_items: List[Dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / "cars_search.json", "w", encoding="utf-8") as f:
        json.dump(search_items, f, ensure_ascii=False, indent=2)
    with open(DATA_DIR / "car_details.json", "w", encoding="utf-8") as f:
        json.dump(detail_items, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Generate car search and detail data")
    parser.add_argument("--days", type=int, default=30, help="Number of future days to generate")
    parser.add_argument(
        "--full-combinations",
        action="store_true",
        help="Generate all combinations of pickup/dropoff, brands, types, transmission, policies",
    )
    parser.add_argument(
        "--max-per-combo",
        type=int,
        default=3,
        help="When not full-combinations, cap number of brands per combo",
    )
    parser.add_argument("--seed", type=str, default="cars", help="Deterministic seed base")

    args = parser.parse_args()
    search_items, detail_items = generate_records(
        days=args.days,
        full_combinations=args.full_combinations,
        max_per_combo=args.max_per_combo,
        seed=args.seed,
    )
    write_files(search_items, detail_items)
    print(
        f"Generated {len(search_items)} search items and {len(detail_items)} detail items "
        f"for {args.days} day(s)."
    )


if __name__ == "__main__":
    main()


