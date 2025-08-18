#!/usr/bin/env python3

# Simple test script for the booking endpoints

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_list_bookings():
    """Test listing all bookings"""
    try:
        response = requests.get(f"{BASE_URL}/bookings/list")
        print(f"✅ List bookings - Status: {response.status_code}")
        if response.status_code == 200:
            bookings = response.json()
            print(f"   Found {len(bookings)} bookings")
            for booking in bookings:
                print(f"   - {booking['booking_type']} (ID: {booking['id']}, User: {booking['user_id']}, Session: {booking['session_id']})")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error testing list bookings: {e}")

def test_create_guest_booking():
    """Test creating a guest booking"""
    guest_booking = {
        "booking_type": "flight",
        "item_id": 456,
        "details": "Guest booking test - JFK to LAX",
        "price": 199.99,
        "session_id": "guest-session-12345"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/bookings/create",
            json=guest_booking,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Create guest booking - Status: {response.status_code}")
        if response.status_code == 200:
            booking = response.json()
            print(f"   Created booking ID: {booking['id']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error creating guest booking: {e}")

def test_list_guest_bookings():
    """Test listing bookings for a specific guest session"""
    try:
        response = requests.get(f"{BASE_URL}/bookings/list?session_id=guest-session-12345")
        print(f"✅ List guest bookings - Status: {response.status_code}")
        if response.status_code == 200:
            bookings = response.json()
            print(f"   Found {len(bookings)} guest bookings")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error testing guest bookings: {e}")

if __name__ == "__main__":
    print("🧪 Testing Booking API...")
    print("=" * 50)
    
    test_list_bookings()
    print()
    test_create_guest_booking()
    print()
    test_list_guest_bookings()
    
    print("\n✨ Tests completed!")
