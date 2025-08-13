import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "data" / "meta-ui"

def load_json(filename: str):
    with open(BASE / filename, encoding="utf-8") as f:
        return json.load(f)

def get_stays_locations():
    return load_json("stays_locations.json")

def get_stays_amenities():
    return load_json("stays_amenities.json")

def get_stays_stars():
    return load_json("stays_stars.json")

def get_airports():
    return load_json("airports.json")

def get_airlines():
    return load_json("airlines.json")

def get_car_locations():
    return load_json("car_locations.json")

def get_car_brands():
    return load_json("car_brands.json")

def get_currencies():
    return load_json("currencies.json")

def get_languages():
    return load_json("languages.json")
