# Things to Do APIs - Comprehensive Summary

## Overview
The Things to Do APIs provide functionality for searching and retrieving information about activities, attractions, and experiences in various locations. The APIs are designed to help users discover and book activities during their travels.

## API Endpoints

### 1. Search Things to Do
**Endpoint:** `GET /things-to-do/search`

**Purpose:** Search for activities and attractions in a specific location with advanced filtering options.

**Required Parameters:**
- `location` (string): City, state, or area to search in (e.g., "Los Angeles, California")
- `date` (string): Date in YYYY-MM-DD format (e.g., "2025-08-15")

**Optional Parameters:**
- `category` (string): Filter by activity category
  - Available categories: Theme Parks, Museums, Tours, Outdoor Activities, Cultural Experiences, Adventure Sports, Food & Dining, Entertainment, Shopping, Wellness & Spa
- `duration` (string): Filter by activity duration
  - Available durations: 1 hour, 2 hours, 3 hours, 4 hours, 5 hours, 6 hours, 1 day, 2 days, 3 days, 1 week
- `min_rating` (float): Minimum rating filter (0.0 to 5.0)
- `price_min` (float): Minimum price filter in USD
- `price_max` (float): Maximum price filter in USD

**Example Request:**
```
GET /things-to-do/search?location=Los Angeles, California&date=2025-08-15&category=Theme Parks&price_max=150
```

**Response Format:**
```json
{
  "things_to_do": [
    {
      "id": "ttd-1",
      "name": "Universal Studios Hollywood Skip-the-Line Ticket",
      "location": "Los Angeles, California",
      "category": "Theme Parks",
      "price": 109.99,
      "rating": 4.7,
      "reviews_count": 2845,
      "duration": "1 day",
      "highlights": [
        "Skip-the-line admission",
        "Access to all rides and attractions",
        "Live shows and entertainment"
      ],
      "available_dates": [
        "2025-08-15",
        "2025-08-16",
        "2025-08-17"
      ]
    }
  ]
}
```

### 2. Get Things to Do by Category
**Endpoint:** `GET /things-to-do/by-category`

**Purpose:** Retrieve activities organized by category with optional filtering.

**Optional Parameters:**
- `category` (string): Filter by specific category. If not provided, returns all categories.

**Example Requests:**
```
GET /things-to-do/by-category
GET /things-to-do/by-category?category=Theme Parks
GET /things-to-do/by-category?category=Outdoor Activities
```

**Response Format:**
```json
[
  {
    "category": "Theme Parks",
    "items": [
      {
        "id": 1,
        "title": "Universal Studios Hollywood Skip-the-Line Ticket",
        "rating": 4.7,
        "reviewsCount": 2845,
        "duration": "1 day",
        "price": 109.99,
        "originalPrice": null,
        "currency": "USD",
        "imageUrl": "https://example.com/ttd-1.jpg",
        "tags": ["Free cancellation"],
        "memberPrice": false
      },
      {
        "id": 5,
        "title": "Disney World Magic Kingdom Ticket",
        "rating": 4.5,
        "reviewsCount": 5678,
        "duration": "1 day",
        "price": 159.99,
        "originalPrice": null,
        "currency": "USD",
        "imageUrl": "https://example.com/ttd-5.jpg",
        "tags": ["Free cancellation"],
        "memberPrice": false
      }
    ]
  },
  {
    "category": "Museums",
    "items": [
      {
        "id": 2,
        "title": "Louvre Museum Skip-the-Line Guided Tour",
        "rating": 4.8,
        "reviewsCount": 1567,
        "duration": "3 hours",
        "price": 89.99,
        "originalPrice": null,
        "currency": "USD",
        "imageUrl": "https://example.com/ttd-2.jpg",
        "tags": ["Free cancellation"],
        "memberPrice": false
      }
    ]
  }
]
```

### 3. Get Activity Details
**Endpoint:** `GET /things-to-do/{thing_id}`

**Purpose:** Retrieve comprehensive information about a specific activity or attraction.

**Parameters:**
- `thing_id` (string): Unique identifier for the activity (format: ttd-{number})

**Example Request:**
```
GET /things-to-do/ttd-1
```

**Response Format:**
```json
{
  "id": "ttd-1",
  "name": "Universal Studios Hollywood Skip-the-Line Ticket",
  "location": "Los Angeles, California",
  "address": "100 Universal City Plaza, Universal City, CA 91608",
  "category": "Theme Parks",
  "price": 109.99,
  "rating": 4.7,
  "reviews_count": 2845,
  "duration": "1 day",
  "highlights": [
    "Skip-the-line admission",
    "Access to all rides and attractions",
    "Live shows and entertainment",
    "The Wizarding World of Harry Potter™",
    "Studio Tour"
  ],
  "description": "Skip the regular lines and head straight to the fun...",
  "included": [
    "Skip-the-line park admission",
    "Access to all rides and attractions",
    "Live shows and entertainment"
  ],
  "not_included": [
    "Food and drinks",
    "Parking fees",
    "Express Pass upgrades",
    "Souvenir photos"
  ],
  "important_info": [
    "Children aged 2 and under enter free",
    "The park is wheelchair accessible",
    "Outside food and drinks are not permitted",
    "Some rides have height and age restrictions"
  ],
  "available_times": [
    "09:00",
    "10:00",
    "11:00",
    "12:00"
  ],
  "cancellation_policy": {
    "free_cancellation_before": "24h",
    "refund_percentage": 100
  }
}
```

## Available Sample Data

The API currently includes 5 sample activities:

1. **Universal Studios Hollywood** (ttd-1) - Theme Parks category
2. **Louvre Museum Tour** (ttd-2) - Museums category  
3. **NYC Food Walking Tour** (ttd-3) - Food & Dining category
4. **Grand Canyon Helicopter Tour** (ttd-4) - Adventure Sports category
5. **Disney World Magic Kingdom** (ttd-5) - Theme Parks category

## Features

### Search Capabilities
- **Location-based search**: Find activities in specific cities or regions
- **Date filtering**: Check availability for specific dates
- **Category filtering**: Filter by activity type (Theme Parks, Museums, etc.)
- **Duration filtering**: Find activities that fit your schedule
- **Rating filtering**: Only show highly-rated activities
- **Price range filtering**: Find activities within your budget

### Category Organization
- **Grouped by category**: Activities organized by type for easy browsing
- **Category filtering**: Get activities from specific categories only
- **Structured response**: Consistent format for frontend integration
- **Rich metadata**: Includes pricing, ratings, duration, and availability

### Detailed Information
- **Comprehensive descriptions**: Full activity descriptions and highlights
- **Pricing information**: Clear pricing with what's included/excluded
- **Practical details**: Address, available times, important restrictions
- **Cancellation policies**: Clear refund and cancellation information
- **Reviews and ratings**: User feedback and ratings

## Error Handling

The APIs include comprehensive error handling:

- **400 Bad Request**: Invalid parameters or malformed requests
- **404 Not Found**: No activities found for search criteria, invalid activity ID, or non-existent category
- **500 Internal Server Error**: Server-side issues

## Testing

A test script (`test_things_to_do_api.py`) is available to verify API functionality:

```bash
python test_things_to_do_api.py
```

The test script includes:
- Basic search functionality testing
- Category and price filter testing
- Category-based activity retrieval testing
- Activity details retrieval testing
- Error handling verification
- API documentation accessibility testing

## Implementation Details

### File Structure
```
app/
├── routers/
│   └── things_to_do.py          # API endpoints
├── services/
│   └── things_to_do_service.py  # Business logic
└── data/things_to_do/
    ├── things_to_do_search.json # Search data
    └── thing_details.json       # Detailed activity data
```

### Service Layer
The service layer provides:
- Data loading and filtering
- Search functionality with multiple filters
- Category-based activity grouping
- Activity details retrieval
- Error handling and validation

### Data Management
- JSON-based data storage for easy maintenance
- Consistent data structure across endpoints
- Extensible design for adding new activities
- Data transformation for different response formats

## Future Enhancements

Potential improvements for the Things to Do APIs:

1. **Booking Integration**: Add booking functionality
2. **Real-time Availability**: Connect to real availability systems
3. **Image Support**: Add activity images and galleries
4. **Reviews System**: Allow users to leave reviews
5. **Recommendations**: AI-powered activity recommendations
6. **Multi-language Support**: Internationalization
7. **Geolocation**: Location-based search using coordinates
8. **Seasonal Pricing**: Dynamic pricing based on dates
9. **Group Discounts**: Special pricing for groups
10. **Accessibility Information**: Detailed accessibility features
11. **Category Analytics**: Popular categories and trending activities
12. **Personalization**: User preference-based recommendations

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

The documentation includes:
- Complete endpoint descriptions
- Request/response examples
- Parameter validation rules
- Error code explanations
- Interactive testing interface
