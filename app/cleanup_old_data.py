#!/usr/bin/env python3
"""
Cleanup script to reduce JSON data size and improve server performance.
This script will:
1. Remove data older than last week
2. Limit the number of records in each file
3. Maintain realistic data combinations
4. Keep search and detail data properly linked
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import random

# Configuration for data reduction
MAX_RECORDS_PER_FILE = {
    # Core search files - keep more for variety
    "cars_search.json": 200,
    "stays_search.json": 300,
    "flights_search.json": 150,
    "activities_search.json": 100,
    "things_to_do_search.json": 80,
    "packages_search.json": 120,
    "cruises_search.json": 80,
    
    # Detail files - keep fewer since they're accessed individually
    "car_details.json": 150,
    "stays_details.json": 200,
    "flight_details.json": 100,
    "activity_details.json": 80,
    "thing_details.json": 60,
    "package_details.json": 100,
    "cruise_details.json": 60,
    
    # Supporting data files
    "stays_reviews.json": 400,
    "stays_nearby.json": 300,
    "stays_availability.json": 500,
    "stays_reviews.json": 400,
    
    # Flight variations
    "one_way.json": 100,
    "round_trip.json": 100,
    "multi_city.json": 80,
    "flight_status.json": 60,
    
    # Other data
    "trips_list.json": 50,
    "bookings.json": 100,
}

# Date fields to check for old data removal
DATE_FIELDS = {
    "cars_search.json": ["pickup_date", "return_date"],
    "stays_search.json": ["check_in", "check_out"],
    "flights_search.json": ["departure_date", "return_date"],
    "activities_search.json": ["date"],
    "things_to_do_search.json": ["date"],
    "packages_search.json": ["start_date", "end_date"],
    "cruises_search.json": ["departure_date"],
    "trips_list.json": ["start_date", "end_date"],
    "bookings.json": ["booking_date", "travel_date"],
}

def get_data_directory() -> Path:
    """Get the data directory path."""
    return Path("data")

def load_json_file(file_path: Path) -> List[Dict[str, Any]]:
    """Load JSON file and return as list of dictionaries."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]
    except Exception as e:
        print(f"⚠️  Error loading {file_path}: {e}")
        return []

def save_json_file(file_path: Path, data: List[Dict[str, Any]]) -> None:
    """Save data to JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {file_path} with {len(data)} records")
    except Exception as e:
        print(f"❌ Error saving {file_path}: {e}")

def is_old_data(item: Dict[str, Any], date_fields: List[str]) -> bool:
    """Check if data item is older than last week."""
    if not date_fields:
        return False
    
    cutoff_date = datetime.now() - timedelta(days=7)
    
    for field in date_fields:
        if field in item:
            try:
                # Handle different date formats
                date_str = str(item[field])
                if len(date_str) == 10:  # YYYY-MM-DD format
                    item_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if item_date < cutoff_date:
                        return True
                elif len(date_str) == 19:  # YYYY-MM-DD HH:MM:SS format
                    item_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    if item_date < cutoff_date:
                        return True
            except (ValueError, TypeError):
                continue
    
    return False

def cleanup_file(file_path: Path, max_records: int, date_fields: List[str]) -> None:
    """Clean up a single JSON file."""
    print(f"\n🔍 Processing {file_path.name}...")
    
    # Load data
    data = load_json_file(file_path)
    if not data:
        return
    
    original_count = len(data)
    print(f"   Original records: {original_count}")
    
    # Remove old data first
    if date_fields:
        data = [item for item in data if not is_old_data(item, date_fields)]
        after_old_removal = len(data)
        print(f"   After removing old data: {after_old_removal}")
    
    # Limit total records
    if len(data) > max_records:
        # Use random sampling to maintain variety
        random.seed(42)  # Consistent results
        data = random.sample(data, max_records)
        print(f"   After limiting records: {len(data)}")
    
    # Save cleaned data
    save_json_file(file_path, data)
    
    reduction = original_count - len(data)
    if reduction > 0:
        print(f"   📉 Reduced by {reduction} records ({reduction/original_count*100:.1f}%)")

def maintain_data_relationships() -> None:
    """Ensure search and detail data remain properly linked."""
    print("\n🔗 Maintaining data relationships...")
    
    # Cars: Ensure search IDs exist in details
    cars_search_path = get_data_directory() / "cars" / "cars_search.json"
    car_details_path = get_data_directory() / "cars" / "car_details.json"
    
    if cars_search_path.exists() and car_details_path.exists():
        cars_search = load_json_file(cars_search_path)
        car_details = load_json_file(car_details_path)
        
        # Get all detail IDs
        detail_ids = {str(item.get("id", "")) for item in car_details}
        
        # Filter search to only include cars with details
        cars_search = [item for item in cars_search if str(item.get("id", "")) in detail_ids]
        
        save_json_file(cars_search_path, cars_search)
        print("   ✅ Cars search and details linked")
    
    # Stays: Ensure search IDs exist in details
    stays_search_path = get_data_directory() / "stays" / "stays_search.json"
    stays_details_path = get_data_directory() / "stays" / "stays_details.json"
    
    if stays_search_path.exists() and stays_details_path.exists():
        stays_search = load_json_file(stays_search_path)
        stays_details = load_json_file(stays_details_path)
        
        # Get all detail IDs
        detail_ids = {str(item.get("id", "")) for item in stays_details}
        
        # Filter search to only include stays with details
        stays_search = [item for item in stays_search if str(item.get("id", "")) in detail_ids]
        
        save_json_file(stays_search_path, stays_search)
        print("   ✅ Stays search and details linked")
    
    # Flights: Ensure search IDs exist in details
    flights_search_path = get_data_directory() / "flights" / "flights_search.json"
    flight_details_path = get_data_directory() / "flights" / "flight_details.json"
    
    if flights_search_path.exists() and flight_details_path.exists():
        flights_search = load_json_file(flights_search_path)
        flight_details = load_json_file(flight_details_path)
        
        # Get all detail IDs
        detail_ids = {str(item.get("id", "")) for item in flight_details}
        
        # Filter search to only include flights with details
        flights_search = [item for item in flights_search if str(item.get("id", "")) in detail_ids]
        
        save_json_file(flights_search_path, flights_search)
        print("   ✅ Flights search and details linked")

def get_file_size_mb(file_path: Path) -> float:
    """Get file size in MB."""
    try:
        return file_path.stat().st_size / (1024 * 1024)
    except:
        return 0

def print_summary() -> None:
    """Print summary of all JSON files after cleanup."""
    print("\n📊 Summary of JSON files after cleanup:")
    print("-" * 60)
    
    data_dir = get_data_directory()
    total_size = 0
    total_files = 0
    
    for file_path in data_dir.rglob("*.json"):
        if file_path.is_file():
            size_mb = get_file_size_mb(file_path)
            total_size += size_mb
            total_files += 1
            print(f"{file_path.name:<35} {size_mb:>8.2f} MB")
    
    print("-" * 60)
    print(f"Total files: {total_files}")
    print(f"Total size: {total_size:.2f} MB")

def main():
    """Main cleanup function."""
    print("🧹 JSON Data Cleanup Script")
    print("=" * 50)
    
    data_dir = get_data_directory()
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        return
    
    # Process each file type
    for filename, max_records in MAX_RECORDS_PER_FILE.items():
        # Find the file in the data directory
        file_path = None
        for found_path in data_dir.rglob(filename):
            if found_path.name == filename:
                file_path = found_path
                break
        
        if file_path and file_path.exists():
            date_fields = DATE_FIELDS.get(filename, [])
            cleanup_file(file_path, max_records, date_fields)
        else:
            print(f"⚠️  File not found: {filename}")
    
    # Maintain data relationships
    maintain_data_relationships()
    
    # Print summary
    print_summary()
    
    print("\n🎉 Cleanup complete! Server performance should be significantly improved.")

if __name__ == "__main__":
    main()

