#!/usr/bin/env python3
"""
Test script for Things to Do APIs
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_search_things_to_do():
    """Test the search things to do endpoint"""
    print("=== Testing Search Things to Do API ===")
    
    # Test case 1: Basic search
    params = {
        "location": "Los Angeles, California",
        "date": "2025-08-15"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/things-to-do/search", params=params)
        print(f"Basic search - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data.get('things_to_do', []))} activities")
            
            # Check if images are included
            for activity in data.get('things_to_do', []):
                if 'imageUrl' in activity:
                    print(f"✅ Activity '{activity['name']}' has image: {activity['imageUrl'][:50]}...")
                else:
                    print(f"❌ Activity '{activity['name']}' missing imageUrl")
            
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start the server first.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test case 2: Search with category filter
    params["category"] = "Theme Parks"
    try:
        response = requests.get(f"{BASE_URL}/things-to-do/search", params=params)
        print(f"\nCategory filter search - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data.get('things_to_do', []))} activities")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test case 3: Search with price filter
    params = {
        "location": "Los Angeles, California",
        "date": "2025-08-15",
        "price_max": 150.0
    }
    try:
        response = requests.get(f"{BASE_URL}/things-to-do/search", params=params)
        print(f"\nPrice filter search - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data.get('things_to_do', []))} activities")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return True

def test_get_things_to_do_by_category():
    """Test the get things to do by category endpoint"""
    print("\n=== Testing Get Things to Do by Category API ===")
    
    # Test case 1: Get all categories
    try:
        response = requests.get(f"{BASE_URL}/things-to-do/by-category")
        print(f"Get all categories - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} categories")
            for category in data:
                print(f"  - {category['category']}: {len(category['items'])} items")
                
                # Check if images are included
                for item in category['items']:
                    if 'imageUrl' in item:
                        print(f"    ✅ Item '{item['title']}' has image: {item['imageUrl'][:50]}...")
                    else:
                        print(f"    ❌ Item '{item['title']}' missing imageUrl")
            
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start the server first.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test case 2: Get specific category
    try:
        response = requests.get(f"{BASE_URL}/things-to-do/by-category?category=Theme Parks")
        print(f"\nGet Theme Parks category - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} category groups")
            for category in data:
                print(f"  - {category['category']}: {len(category['items'])} items")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test case 3: Get non-existent category
    try:
        response = requests.get(f"{BASE_URL}/things-to-do/by-category?category=NonExistent")
        print(f"\nGet non-existent category - Status: {response.status_code}")
        if response.status_code == 404:
            print("✅ Correctly returned 404 for non-existent category")
        else:
            print(f"Unexpected response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return True

def test_get_thing_details():
    """Test the get thing details endpoint"""
    print("\n=== Testing Get Thing Details API ===")
    
    # Test case 1: Valid ID
    thing_id = "ttd-1"
    try:
        response = requests.get(f"{BASE_URL}/things-to-do/{thing_id}")
        print(f"Get details for {thing_id} - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Activity details:")
            print(f"  Name: {data.get('name')}")
            print(f"  Location: {data.get('location')}")
            print(f"  Price: ${data.get('price')}")
            print(f"  Rating: {data.get('rating')}")
            print(f"  Duration: {data.get('duration')}")
            
            # Check if image is included
            if 'imageUrl' in data:
                print(f"  ✅ Has image: {data['imageUrl'][:50]}...")
            else:
                print(f"  ❌ Missing imageUrl")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start the server first.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test case 2: Invalid ID
    thing_id = "ttd-999"
    try:
        response = requests.get(f"{BASE_URL}/things-to-do/{thing_id}")
        print(f"\nGet details for invalid {thing_id} - Status: {response.status_code}")
        if response.status_code == 404:
            print("✅ Correctly returned 404 for invalid ID")
        else:
            print(f"Unexpected response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return True

def test_api_documentation():
    """Test if the API documentation is accessible"""
    print("\n=== Testing API Documentation ===")
    
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"OpenAPI docs - Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ API documentation is accessible")
        else:
            print("❌ API documentation not accessible")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start the server first.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Testing Things to Do APIs with Real Images")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print("✅ Server is running")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start it with:")
        print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return
    
    # Run tests
    test_search_things_to_do()
    test_get_things_to_do_by_category()
    test_get_thing_details()
    test_api_documentation()
    
    print("\n" + "=" * 60)
    print("✅ Testing completed with image verification!")

if __name__ == "__main__":
    main()
