#!/usr/bin/env python3

# Simple test for frontend session management
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("🧪 Testing Frontend-Managed Session Booking System")
print("=" * 60)

# Test 1: List existing bookings (should have 1 from seed data)
print("1️⃣ Testing: List all bookings")
response = requests.get(f"{BASE_URL}/bookings/list")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    bookings = response.json()
    print(f"   Found {len(bookings)} existing bookings")
    for booking in bookings:
        user_type = "User" if booking['user_id'] else "Guest"
        print(f"   - {user_type} booking: {booking['booking_type']} (ID: {booking['id']})")
else:
    print(f"   ❌ Error: {response.text}")

print()

# Test 2: Create a guest booking with frontend-managed session
print("2️⃣ Testing: Create guest booking (frontend manages session_id)")
guest_booking = {
    "booking_type": "flight",
    "item_id": 789,
    "details": "Guest flight booking - SFO to NYC",
    "price": 450.00,
    "session_id": "frontend-session-abc123"  # Frontend generates this
}

response = requests.post(f"{BASE_URL}/bookings/create", json=guest_booking)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    booking = response.json()
    print(f"   ✅ Created guest booking with ID: {booking['id']}")
    print(f"   Session ID: {booking['session_id']}")
else:
    print(f"   ❌ Error: {response.text}")

print()

# Test 3: List bookings for the specific guest session
print("3️⃣ Testing: List bookings for specific guest session")
response = requests.get(f"{BASE_URL}/bookings/list?session_id=frontend-session-abc123")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    bookings = response.json()
    print(f"   ✅ Found {len(bookings)} bookings for this guest session")
else:
    print(f"   ❌ Error: {response.text}")

print()

# Test 4: Create another booking for same session
print("4️⃣ Testing: Create another booking for same guest session")
another_booking = {
    "booking_type": "stay",
    "item_id": 456,
    "details": "Hotel booking for same guest",
    "price": 120.00,
    "session_id": "frontend-session-abc123"  # Same session ID
}

response = requests.post(f"{BASE_URL}/bookings/create", json=another_booking)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    booking = response.json()
    print(f"   ✅ Created another booking for same session: {booking['id']}")
else:
    print(f"   ❌ Error: {response.text}")

print()

# Test 5: List bookings for the guest session again
print("5️⃣ Testing: List all bookings for guest session (should be 2 now)")
response = requests.get(f"{BASE_URL}/bookings/list?session_id=frontend-session-abc123")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    bookings = response.json()
    print(f"   ✅ Found {len(bookings)} bookings for guest session")
    for booking in bookings:
        print(f"   - {booking['booking_type']}: ${booking['price']}")
else:
    print(f"   ❌ Error: {response.text}")

print("\n" + "=" * 60)
print("✨ Frontend Session Management Summary:")
print("   • Frontend generates session_id (e.g., using UUID)")
print("   • Frontend sends session_id with each booking request")
print("   • Backend stores and returns bookings by session_id")
print("   • No backend session middleware needed!")
