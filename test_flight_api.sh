#!/bin/bash
# Flight API Curl Test Script
# Based on flight_test_parameters.json

BASE_URL="http://localhost:8000"

echo "🛫 Flight API Curl Test Script"
echo "=============================="
echo "Base URL: $BASE_URL"
echo

# Test 1: One-Way Flights
echo "1️⃣ ONE-WAY FLIGHT TESTS"
echo "------------------------"

echo "Testing JFK → FLL (American Airlines)..."
curl -s "$BASE_URL/flights/search/one-way?origin=JFK&destination=FLL&depart=2025-08-17&passengers=1&seat_class=economy" | jq '.flights | length' 2>/dev/null || echo "❌ Failed"

echo "Testing LAX → JFK (Delta Airlines Business)..."
curl -s "$BASE_URL/flights/search/one-way?origin=LAX&destination=JFK&depart=2025-08-20&passengers=2&seat_class=business" | jq '.flights | length' 2>/dev/null || echo "❌ Failed"

echo "Testing SIN → JFK (Singapore Airlines Business)..."
curl -s "$BASE_URL/flights/search/one-way?origin=SIN&destination=JFK&depart=2025-08-17&passengers=1&seat_class=business&stops=0" | jq '.flights | length' 2>/dev/null || echo "❌ Failed"

echo "Testing NRT → HND (Japan Airlines Premium)..."
curl -s "$BASE_URL/flights/search/one-way?origin=NRT&destination=HND&depart=2025-08-20&seat_class=premium_economy&airline=JL" | jq '.flights | length' 2>/dev/null || echo "❌ Failed"

echo

# Test 2: Round-Trip Flights
echo "2️⃣ ROUND-TRIP FLIGHT TESTS"
echo "---------------------------"

echo "Testing JFK ↔ FLL Round-trip..."
curl -s "$BASE_URL/flights/search/round-trip?origin=JFK&destination=FLL&depart=2025-10-10&returnd=2025-10-17&passengers=2&seat_class=economy" | jq '.flights | length' 2>/dev/null || echo "❌ Failed"

echo "Testing MAD ↔ BCN Round-trip (Iberia Business)..."
curl -s "$BASE_URL/flights/search/round-trip?origin=MAD&destination=BCN&depart=2025-08-20&returnd=2025-08-27&seat_class=business&airline=IB" | jq '.flights | length' 2>/dev/null || echo "❌ Failed"

echo

# Test 3: Multi-City Flights
echo "3️⃣ MULTI-CITY FLIGHT TESTS"
echo "---------------------------"

echo "Testing US Multi-City (United Airlines)..."
curl -s "$BASE_URL/flights/search/multi-city?passengers=1&airline=UA" | jq '.flights | length' 2>/dev/null || echo "❌ Failed"

echo "Testing Japan Multi-City (Japan Airlines Business)..."
curl -s "$BASE_URL/flights/search/multi-city?passengers=2&seat_class=business&airline=JL" | jq '.flights | length' 2>/dev/null || echo "❌ Failed"

echo

# Test 4: Flight Details
echo "4️⃣ FLIGHT DETAILS TESTS"
echo "------------------------"

echo "Testing Flight Details flt-ow-001..."
curl -s "$BASE_URL/flights/details/flt-ow-001" | jq '.flight.id' 2>/dev/null || echo "❌ Failed"

echo "Testing Flight Details flt-rt-001..."
curl -s "$BASE_URL/flights/details/flt-rt-001" | jq '.flight.id' 2>/dev/null || echo "❌ Failed"

echo "Testing Flight Details flt-mc-001..."
curl -s "$BASE_URL/flights/details/flt-mc-001" | jq '.flight.id' 2>/dev/null || echo "❌ Failed"

echo

# Test 5: Flight Status
echo "5️⃣ FLIGHT STATUS TESTS"
echo "-----------------------"

echo "Testing Flight Status AA100..."
curl -s "$BASE_URL/flights/status/AA100" | jq '.flight_number' 2>/dev/null || echo "❌ Failed"

echo "Testing Flight Status DL1501..."
curl -s "$BASE_URL/flights/status/DL1501" | jq '.flight_number' 2>/dev/null || echo "❌ Failed"

echo "Testing Flight Status JL205..."
curl -s "$BASE_URL/flights/status/JL205" | jq '.flight_number' 2>/dev/null || echo "❌ Failed"

echo

echo "✅ Curl tests completed!"
echo "Note: Install 'jq' for better JSON parsing, or check responses manually"
echo
echo "🔗 Quick Test Commands:"
echo "curl \"$BASE_URL/flights/search/one-way?origin=JFK&destination=FLL&depart=2025-08-17\""
echo "curl \"$BASE_URL/flights/search/round-trip?origin=JFK&destination=FLL&depart=2025-10-10&returnd=2025-10-17\""
echo "curl \"$BASE_URL/flights/search/multi-city?passengers=1\""
echo "curl \"$BASE_URL/flights/details/flt-ow-001\""
echo "curl \"$BASE_URL/flights/status/AA100\""
