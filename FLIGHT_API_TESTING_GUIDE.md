# 🛫 Flight API Testing Guide

## 📋 **Quick Reference**

### **Base URL:** `http://localhost:8000`

### **Available Endpoints:**
- `/flights/search/one-way` - One-way flights
- `/flights/search/round-trip` - Round-trip flights  
- `/flights/search/multi-city` - Multi-city flights
- `/flights/details/{flight_id}` - Flight details
- `/flights/status/{flight_number}` - Flight status

---

## 🗺️ **Available Airport Codes**

| Code | Airport | City | Country |
|------|---------|------|---------|
| **LHE** | Allama Iqbal International | Lahore | Pakistan |
| **JFK** | John F. Kennedy International | New York | USA |
| **LAX** | Los Angeles International | Los Angeles | USA |
| **MIA** | Miami International | Miami | USA |
| **LHR** | London Heathrow | London | UK |
| **CDG** | Charles de Gaulle | Paris | France |
| **DXB** | Dubai International | Dubai | UAE |
| **HND** | Haneda | Tokyo | Japan |
| **NRT** | Narita International | Tokyo | Japan |
| **SIN** | Changi | Singapore | Singapore |
| **SYD** | Kingsford Smith | Sydney | Australia |
| **FRA** | Frankfurt | Frankfurt | Germany |
| **HKG** | Hong Kong International | Hong Kong | China |
| **IST** | Istanbul | Istanbul | Turkey |
| **BCN** | Barcelona-El Prat | Barcelona | Spain |
| **LGA** | LaGuardia | New York | USA |
| **FLL** | Fort Lauderdale-Hollywood | Fort Lauderdale | USA |

---

## ✈️ **Available Airlines**

| Code | Airline | Alliance |
|------|---------|----------|
| **AA** | American Airlines | Oneworld |
| **UA** | United Airlines | Star Alliance |
| **BA** | British Airways | Oneworld |
| **AF** | Air France | SkyTeam |
| **LH** | Lufthansa | Star Alliance |
| **EK** | Emirates | Independent |
| **SQ** | Singapore Airlines | Star Alliance |
| **CX** | Cathay Pacific | Oneworld |
| **QF** | Qantas | Oneworld |
| **TK** | Turkish Airlines | Star Alliance |
| **ANA** | All Nippon Airways | Star Alliance |

---

## 🎛️ **Query Parameters**

### **Common Parameters:**
- `passengers` - Number of passengers (1-9)
- `seat_class` - `economy`, `premium_economy`, `business`, `first`
- `stops` - Number of stops: `0` (nonstop), `1`, `2` (2+)
- `airline` - Airline code (AA, UA, BA, etc.)
- `price_min` - Minimum price filter
- `price_max` - Maximum price filter
- `sort_by` - `price_asc`, `price_desc`, `duration`, `departure_time`

### **Date Format:** `YYYY-MM-DD` (e.g., `2025-12-25`)

---

# 🧪 **Test Cases Based on Available Data**

## 1️⃣ **One-Way Flights (Available Routes)**

### **JFK → FLL (American Airlines)**
```bash
curl "http://localhost:8000/flights/search/one-way?origin=JFK&destination=FLL&depart=2025-08-17"
```

### **LAX → JFK (Delta Airlines)**
```bash
curl "http://localhost:8000/flights/search/one-way?origin=LAX&destination=JFK&depart=2025-08-20&passengers=2&seat_class=business"
```

### **NRT → HND (Japan Airlines - Tokyo Domestic)**
```bash
curl "http://localhost:8000/flights/search/one-way?origin=NRT&destination=HND&depart=2025-08-20&seat_class=premium_economy&airline=JL"
```

### **MAD → BCN (Iberia - Spain Domestic)**
```bash
curl "http://localhost:8000/flights/search/one-way?origin=MAD&destination=BCN&depart=2025-08-20&seat_class=economy&price_max=500"
```

### **SIN → JFK (Singapore Airlines - Long Haul)**
```bash
curl "http://localhost:8000/flights/search/one-way?origin=SIN&destination=JFK&depart=2025-08-17&seat_class=business&stops=0"
```

### **SYD → LAX (Qantas - Trans-Pacific)**
```bash
curl "http://localhost:8000/flights/search/one-way?origin=SYD&destination=LAX&depart=2025-08-17&passengers=1&stops=1"
```

### **CDG → JFK (Air France - Trans-Atlantic)**
```bash
curl "http://localhost:8000/flights/search/one-way?origin=CDG&destination=JFK&depart=2025-08-17&seat_class=first&airline=AF"
```

---

## 2️⃣ **Round-Trip Flights (Available Routes)**

### **JFK ↔ FLL (American Airlines)**
```bash
curl "http://localhost:8000/flights/search/round-trip?origin=JFK&destination=FLL&depart=2025-10-10&returnd=2025-10-17&passengers=2"
```

### **MAD ↔ BCN (Iberia - Spain Domestic)**
```bash
curl "http://localhost:8000/flights/search/round-trip?origin=MAD&destination=BCN&depart=2025-08-20&returnd=2025-08-27&seat_class=business&airline=IB"
```


### **Round-Trip with Filters**
```bash
curl "http://localhost:8000/flights/search/round-trip?origin=JFK&destination=FLL&depart=2025-10-10&returnd=2025-10-17&passengers=4&seat_class=economy&stops=0&sort_by=price_asc"
```

---

## 3️⃣ **Multi-City Flights (Available Routes)**

### **US Multi-City (United Airlines): JFK → FLL → LGA → JFK**
```bash
curl "http://localhost:8000/flights/search/multi-city?passengers=1&airline=UA"
```

### **Japan Multi-City (Japan Airlines): NRT → HND → BCN → NRT**
```bash
curl "http://localhost:8000/flights/search/multi-city?passengers=2&seat_class=business&airline=JL"
```

### **Multi-City with Filters**
```bash
curl "http://localhost:8000/flights/search/multi-city?passengers=1&seat_class=first&stops=2&price_min=1000&sort_by=duration"
```

---

## 4️⃣ **Flight Details & Status (Available Flight IDs)**

### **Flight Details**
```bash
curl "http://localhost:8000/flights/details/flt-ow-001"  # AA JFK→FLL
curl "http://localhost:8000/flights/details/flt-ow-002"  # DL LAX→JFK
curl "http://localhost:8000/flights/details/flt-ow-003"  # JL NRT→HND
curl "http://localhost:8000/flights/details/flt-rt-001"  # AA JFK↔FLL Round-trip
curl "http://localhost:8000/flights/details/flt-mc-001"  # UA Multi-city
```

### **Flight Status (Available Flight Numbers)**
```bash
curl "http://localhost:8000/flights/status/AA100"    # American Airlines
curl "http://localhost:8000/flights/status/DL1501"   # Delta Airlines
curl "http://localhost:8000/flights/status/JL205"    # Japan Airlines
curl "http://localhost:8000/flights/status/SQ21"     # Singapore Airlines
curl "http://localhost:8000/flights/status/UA2345"   # United Airlines
```

---

# 🎯 **Available Route Combinations**

## **Domestic Routes**
| Route | Airline | Type | Date Available |
|-------|---------|------|----------------|
| **JFK ↔ FLL** | American Airlines (AA) | One-way & Round-trip | 2025-08-17, 2025-10-10 |
| **LAX → JFK** | Delta Airlines (DL) | One-way | 2025-08-20 |
| **NRT ↔ HND** | Japan Airlines (JL) | One-way & Round-trip | 2025-08-20 |
| **MAD ↔ BCN** | Iberia (IB) | One-way & Round-trip | 2025-08-20 |

## **International Routes**
| Route | Airline | Type | Date Available |
|-------|---------|------|----------------|
| **SIN → JFK** | Singapore Airlines (SQ) | One-way | 2025-08-17 |
| **SYD → LAX** | Qantas (QF) | One-way | 2025-08-17 |
| **CDG → JFK** | Air France (AF) | One-way | 2025-08-17 |
| **IST → LHR** | Turkish Airlines (TK) | One-way | 2025-08-17 |

## **Multi-City Routes**
| Route | Airline | Segments |
|-------|---------|----------|
| **JFK → FLL → LGA → JFK** | United Airlines (UA) | 3 segments (US) |
| **NRT → HND → BCN → NRT** | Japan Airlines (JL) | 3 segments (Japan-Spain) |

---

# 🔧 **Python Test Script (Updated with Real Data)**

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_flights_with_real_data():
    print("🛫 Testing Flight APIs with Available Data")
    print("=" * 60)
    
    # Test 1: One-Way Flights
    print("\\n1. One-Way Flight Tests")
    print("-" * 30)
    
    routes = [
        ("JFK", "FLL", "2025-08-17", "AA - American Airlines"),
        ("LAX", "JFK", "2025-08-20", "DL - Delta Airlines"),
        ("NRT", "HND", "2025-08-20", "JL - Japan Airlines"),
        ("SIN", "JFK", "2025-08-17", "SQ - Singapore Airlines")
    ]
    
    for origin, dest, date, desc in routes:
        response = requests.get(f"{BASE_URL}/flights/search/one-way", params={
            "origin": origin,
            "destination": dest,
            "depart": date,
            "passengers": 1
        })
        print(f"{origin}→{dest} ({desc}): Status {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Found {len(data.get('flights', []))} flights")
    
    # Test 2: Round-Trip Flights
    print("\\n2. Round-Trip Flight Tests")
    print("-" * 30)
    
    response = requests.get(f"{BASE_URL}/flights/search/round-trip", params={
        "origin": "JFK",
        "destination": "FLL",
        "depart": "2025-10-10",
        "returnd": "2025-10-17",
        "passengers": 2
    })
    print(f"JFK↔FLL Round-trip: Status {response.status_code}")
    
    # Test 3: Multi-City
    print("\\n3. Multi-City Flight Tests")
    print("-" * 30)
    
    response = requests.get(f"{BASE_URL}/flights/search/multi-city", params={
        "passengers": 1
    })
    print(f"Multi-city search: Status {response.status_code}")
    
    # Test 4: Flight Details
    print("\\n4. Flight Details Tests")
    print("-" * 30)
    
    flight_ids = ["flt-ow-001", "flt-rt-001", "flt-mc-001"]
    for flight_id in flight_ids:
        response = requests.get(f"{BASE_URL}/flights/details/{flight_id}")
        print(f"Flight {flight_id}: Status {response.status_code}")
    
    # Test 5: Flight Status
    print("\\n5. Flight Status Tests")
    print("-" * 30)
    
    flight_numbers = ["AA100", "DL1501", "JL205", "SQ21"]
    for flight_num in flight_numbers:
        response = requests.get(f"{BASE_URL}/flights/status/{flight_num}")
        print(f"Flight {flight_num}: Status {response.status_code}")

if __name__ == "__main__":
    test_flights_with_real_data()
```

---

# 🎯 **Available Routes You Can Actually Test**

## **US Domestic Routes**
```bash
# New York to Fort Lauderdale (American Airlines)
curl "http://localhost:8000/flights/search/one-way?origin=JFK&destination=FLL&depart=2025-08-17"

# New York ↔ Fort Lauderdale Round-trip (American Airlines)
curl "http://localhost:8000/flights/search/round-trip?origin=JFK&destination=FLL&depart=2025-10-10&returnd=2025-10-17"

# Los Angeles to New York (Delta Airlines)
curl "http://localhost:8000/flights/search/one-way?origin=LAX&destination=JFK&depart=2025-08-20"
```

## **International Routes**
```bash
# Singapore to New York (Singapore Airlines - Long Haul)
curl "http://localhost:8000/flights/search/one-way?origin=SIN&destination=JFK&depart=2025-08-17&seat_class=business"

# Sydney to Los Angeles (Qantas - Trans-Pacific)
curl "http://localhost:8000/flights/search/one-way?origin=SYD&destination=LAX&depart=2025-08-17&stops=1"

# Paris to New York (Air France - Trans-Atlantic)
curl "http://localhost:8000/flights/search/one-way?origin=CDG&destination=JFK&depart=2025-08-17&seat_class=first"

# Istanbul to London (Turkish Airlines with Stop)
curl "http://localhost:8000/flights/search/one-way?origin=IST&destination=LHR&depart=2025-08-17&stops=1"
```

## **European Routes**
```bash
# Madrid to Barcelona (Iberia - Spain Domestic)
curl "http://localhost:8000/flights/search/one-way?origin=MAD&destination=BCN&depart=2025-08-20"

# Madrid ↔ Barcelona Round-trip (Iberia)
curl "http://localhost:8000/flights/search/round-trip?origin=MAD&destination=BCN&depart=2025-08-20&returnd=2025-08-27"
```

## **Asian Routes**
```bash
# Tokyo Narita to Haneda (Japan Airlines - Domestic)
curl "http://localhost:8000/flights/search/one-way?origin=NRT&destination=HND&depart=2025-08-20"

# Tokyo Round-trip (Japan Airlines)
curl "http://localhost:8000/flights/search/round-trip?origin=NRT&destination=HND&depart=2025-08-20&returnd=2025-08-25"
```

## **Multi-City Routes**
```bash
# US Multi-City: New York → Fort Lauderdale → LaGuardia → New York (United Airlines)
curl "http://localhost:8000/flights/search/multi-city?passengers=1&airline=UA"

# International Multi-City: Tokyo → Barcelona → Tokyo (Japan Airlines)
curl "http://localhost:8000/flights/search/multi-city?passengers=2&seat_class=business&airline=JL"
```

---

# 🔧 **Python Test Scripts**

## **Complete Flight Search Test**
```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_flights():
    print("🛫 Testing Flight APIs")
    print("=" * 50)
    
    # Test One-Way
    print("\\n1. One-Way Flight Search")
    response = requests.get(f"{BASE_URL}/flights/search/one-way", params={
        "origin": "JFK",
        "destination": "LAX", 
        "depart": "2025-12-15",
        "passengers": 1,
        "seat_class": "economy"
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data.get('flights', []))} flights")
    
    # Test Round-Trip
    print("\\n2. Round-Trip Flight Search")
    response = requests.get(f"{BASE_URL}/flights/search/round-trip", params={
        "origin": "LHR",
        "destination": "CDG",
        "depart": "2025-11-20",
        "returnd": "2025-11-27",
        "passengers": 2
    })
    print(f"Status: {response.status_code}")
    
    # Test Multi-City
    print("\\n3. Multi-City Flight Search")
    response = requests.get(f"{BASE_URL}/flights/search/multi-city", params={
        "passengers": 1,
        "seat_class": "business"
    })
    print(f"Status: {response.status_code}")
    
    # Test Flight Details
    print("\\n4. Flight Details")
    response = requests.get(f"{BASE_URL}/flights/details/flt-ow-001")
    print(f"Status: {response.status_code}")
    
    # Test Flight Status
    print("\\n5. Flight Status")
    response = requests.get(f"{BASE_URL}/flights/status/AA100")
    print(f"Status: {response.status_code}")

if __name__ == "__main__":
    test_flights()
```

---

# 📊 **Expected Response Structure**

## **Search Response**
```json
{
  "flights": [
    {
      "id": "flt-ow-001",
      "trip_type": "one_way",
      "airline": {
        "code": "AA",
        "name": "American Airlines",
        "logo": "..."
      },
      "stops": 0,
      "seat_classes": ["economy", "business", "first"],
      "price": {
        "total": 299,
        "currency": "USD"
      },
      "duration_total_minutes": 185,
      "legs": [...]
    }
  ],
  "meta": {
    "total_results": 10,
    "search_params": {...}
  }
}
```

## **Flight Details Response**
```json
{
  "flight": {
    "id": "flt-ow-001",
    "trip_type": "one_way",
    "detailed_info": "...",
    "legs": [...],
    "baggage": {...},
    "policies": {...}
  }
}
```

---

# ⚡ **Quick Test Commands (Guaranteed to Work)**

**Test all endpoints with available data:**
```bash
# One-way (American Airlines: JFK → FLL)
curl "http://localhost:8000/flights/search/one-way?origin=JFK&destination=FLL&depart=2025-08-17"

# Round-trip (American Airlines: JFK ↔ FLL)
curl "http://localhost:8000/flights/search/round-trip?origin=JFK&destination=FLL&depart=2025-10-10&returnd=2025-10-17"

# Multi-city (United Airlines: JFK → FLL → LGA → JFK)
curl "http://localhost:8000/flights/search/multi-city?passengers=1"

# Flight Details (American Airlines flight)
curl "http://localhost:8000/flights/details/flt-ow-001"

# Flight Status (American Airlines AA100)
curl "http://localhost:8000/flights/status/AA100"
```

**Alternative Routes:**
```bash
# International: Singapore to New York
curl "http://localhost:8000/flights/search/one-way?origin=SIN&destination=JFK&depart=2025-08-17"

# European: Madrid to Barcelona
curl "http://localhost:8000/flights/search/one-way?origin=MAD&destination=BCN&depart=2025-08-20"

# Asian: Tokyo Narita to Haneda
curl "http://localhost:8000/flights/search/one-way?origin=NRT&destination=HND&depart=2025-08-20"
```

🚀 **Ready to test all flight combinations!**
