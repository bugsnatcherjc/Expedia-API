# Flight API PowerShell Test Script
# Based on flight_test_parameters.json

$BASE_URL = "http://localhost:8000"

Write-Host "🛫 Flight API PowerShell Test Script" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Base URL: $BASE_URL"
Write-Host

function Test-FlightEndpoint {
    param(
        [string]$Url,
        [string]$TestName
    )
    
    try {
        Write-Host "Testing $TestName..." -NoNewline
        $response = Invoke-RestMethod -Uri $Url -Method Get -TimeoutSec 10
        
        if ($response.flights) {
            $count = $response.flights.Count
            Write-Host " ✅ Found $count flights" -ForegroundColor Green
        } elseif ($response.flight) {
            Write-Host " ✅ Flight details found" -ForegroundColor Green
        } elseif ($response.flight_number) {
            Write-Host " ✅ Flight status found" -ForegroundColor Green
        } else {
            Write-Host " ⚠️ Unexpected response format" -ForegroundColor Yellow
        }
        return $true
    }
    catch {
        Write-Host " ❌ Failed - $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Test 1: One-Way Flights
Write-Host "1️⃣ ONE-WAY FLIGHT TESTS" -ForegroundColor Yellow
Write-Host "------------------------" -ForegroundColor Yellow

$tests = @()
$passed = 0

$tests += Test-FlightEndpoint "$BASE_URL/flights/search/one-way?origin=JFK&destination=FLL&depart=2025-08-17&passengers=1&seat_class=economy" "JFK → FLL (American Airlines)"
$tests += Test-FlightEndpoint "$BASE_URL/flights/search/one-way?origin=LAX&destination=JFK&depart=2025-08-20&passengers=2&seat_class=business" "LAX → JFK (Delta Business)"
$tests += Test-FlightEndpoint "$BASE_URL/flights/search/one-way?origin=SIN&destination=JFK&depart=2025-08-17&passengers=1&seat_class=business&stops=0" "SIN → JFK (Singapore Business)"
$tests += Test-FlightEndpoint "$BASE_URL/flights/search/one-way?origin=NRT&destination=HND&depart=2025-08-20&seat_class=premium_economy&airline=JL" "NRT → HND (Japan Airlines)"

Write-Host

# Test 2: Round-Trip Flights
Write-Host "2️⃣ ROUND-TRIP FLIGHT TESTS" -ForegroundColor Yellow
Write-Host "---------------------------" -ForegroundColor Yellow

$tests += Test-FlightEndpoint "$BASE_URL/flights/search/round-trip?origin=JFK&destination=FLL&depart=2025-10-10&returnd=2025-10-17&passengers=2&seat_class=economy" "JFK ↔ FLL Round-trip"
$tests += Test-FlightEndpoint "$BASE_URL/flights/search/round-trip?origin=MAD&destination=BCN&depart=2025-08-20&returnd=2025-08-27&seat_class=business&airline=IB" "MAD ↔ BCN (Iberia Business)"

Write-Host

# Test 3: Multi-City Flights
Write-Host "3️⃣ MULTI-CITY FLIGHT TESTS" -ForegroundColor Yellow
Write-Host "---------------------------" -ForegroundColor Yellow

$tests += Test-FlightEndpoint "$BASE_URL/flights/search/multi-city?passengers=1&airline=UA" "US Multi-City (United)"
$tests += Test-FlightEndpoint "$BASE_URL/flights/search/multi-city?passengers=2&seat_class=business&airline=JL" "Japan Multi-City (JAL Business)"

Write-Host

# Test 4: Flight Details
Write-Host "4️⃣ FLIGHT DETAILS TESTS" -ForegroundColor Yellow
Write-Host "------------------------" -ForegroundColor Yellow

$tests += Test-FlightEndpoint "$BASE_URL/flights/details/flt-ow-001" "Flight Details flt-ow-001"
$tests += Test-FlightEndpoint "$BASE_URL/flights/details/flt-rt-001" "Flight Details flt-rt-001"
$tests += Test-FlightEndpoint "$BASE_URL/flights/details/flt-mc-001" "Flight Details flt-mc-001"

Write-Host

# Test 5: Flight Status
Write-Host "5️⃣ FLIGHT STATUS TESTS" -ForegroundColor Yellow
Write-Host "-----------------------" -ForegroundColor Yellow

$tests += Test-FlightEndpoint "$BASE_URL/flights/status/AA100" "Flight Status AA100"
$tests += Test-FlightEndpoint "$BASE_URL/flights/status/DL1501" "Flight Status DL1501"
$tests += Test-FlightEndpoint "$BASE_URL/flights/status/JL205" "Flight Status JL205"

Write-Host

# Summary
$total = $tests.Count
$passed = ($tests | Where-Object { $_ -eq $true }).Count
$failed = $total - $passed

Write-Host "📊 TEST SUMMARY" -ForegroundColor Cyan
Write-Host "===============" -ForegroundColor Cyan
Write-Host "Total Tests: $total"
Write-Host "Passed: $passed" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red
Write-Host "Success Rate: $([math]::Round(($passed/$total)*100,1))%"

if ($passed -eq $total) {
    Write-Host "🎉 All tests passed!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Some tests failed. Check the server and test parameters." -ForegroundColor Yellow
}

Write-Host
Write-Host "🔗 Quick Test Commands:" -ForegroundColor Cyan
Write-Host "Invoke-RestMethod -Uri '$BASE_URL/flights/search/one-way?origin=JFK&destination=FLL&depart=2025-08-17'"
Write-Host "Invoke-RestMethod -Uri '$BASE_URL/flights/search/round-trip?origin=JFK&destination=FLL&depart=2025-10-10&returnd=2025-10-17'"
Write-Host "Invoke-RestMethod -Uri '$BASE_URL/flights/search/multi-city?passengers=1'"
Write-Host "Invoke-RestMethod -Uri '$BASE_URL/flights/details/flt-ow-001'"
Write-Host "Invoke-RestMethod -Uri '$BASE_URL/flights/status/AA100'"
