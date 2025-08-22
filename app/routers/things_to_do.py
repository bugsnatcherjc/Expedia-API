from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional, List
from app.services import things_to_do_service

router = APIRouter(prefix="/things-to-do", tags=["Things To Do"])

@router.get("/search", 
    summary="Search for Things to Do",
    description="""
    Search for activities, attractions, and experiences in a specific location.
    
    **Features:**
    - Filter by location and date
    - Category-based filtering (Theme Parks, Museums, Tours, etc.)
    - Duration-based filtering (1 day, 2 hours, etc.)
    - Rating and price range filtering
    - Real-time availability checking
    
    **Example Usage:**
    - Search for theme parks in Los Angeles: `/search?location=Los Angeles&date=2025-08-15&category=Theme Parks`
    - Find free activities: `/search?location=New York&date=2025-08-15&price_max=0`
    - High-rated tours: `/search?location=Paris&date=2025-08-15&category=Tours&min_rating=4.5`
    """,
    response_description="List of available activities matching the search criteria",
    responses={
        200: {
            "description": "Successful search results",
            "content": {
                "application/json": {
                    "example": {
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
                                "highlights": ["Skip-the-line admission", "Access to all rides"],
                                "imageUrl": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=800&h=600&fit=crop"
                            }
                        ]
                    }
                }
            }
        },
        400: {"description": "Invalid search parameters"},
        404: {"description": "No activities found for the specified criteria"}
    }
)
async def search_things_to_do(
    location: str = Query(
        ..., 
        description="City, State, or Area to search in",
        example="Los Angeles, California",
        min_length=2,
        max_length=100
    ),
    date: str = Query(
        ..., 
        description="Date in YYYY-MM-DD format",
        example="2025-08-15",
        regex=r"^\d{4}-\d{2}-\d{2}$"
    ),
    category: Optional[str] = Query(
        None, 
        description="Filter by activity category",
        example="Theme Parks",
        enum=["Theme Parks", "Museums", "Tours", "Outdoor Activities", "Cultural Experiences", "Adventure Sports", "Food & Dining", "Entertainment", "Shopping", "Wellness & Spa"]
    ),
    duration: Optional[str] = Query(
        None, 
        description="Filter by activity duration",
        example="1 day",
        enum=["1 hour", "2 hours", "3 hours", "4 hours", "5 hours", "6 hours", "1 day", "2 days", "3 days", "1 week"]
    ),
    min_rating: Optional[float] = Query(
        None, 
        ge=0, 
        le=5, 
        description="Minimum rating filter (0.0 to 5.0)",
        example=4.0
    ),
    price_min: Optional[float] = Query(
        None, 
        ge=0, 
        description="Minimum price filter in USD",
        example=0.0
    ),
    price_max: Optional[float] = Query(
        None, 
        ge=0, 
        description="Maximum price filter in USD",
        example=200.0
    )
):
    """
    Search for things to do in a specific location with advanced filtering options.
    
    **Required Parameters:**
    - `location`: The city, state, or area where you want to find activities
    - `date`: The date you want to check availability (YYYY-MM-DD format)
    
    **Optional Filters:**
    - `category`: Filter by specific activity type (e.g., Theme Parks, Museums)
    - `duration`: Filter by how long the activity takes
    - `min_rating`: Only show activities with ratings above this value
    - `price_min`/`price_max`: Filter by price range
    
    **Search Tips:**
    - Use broad location terms (e.g., "Los Angeles" instead of specific addresses)
    - Categories are case-sensitive
    - Price filters work with USD values
    - Rating filters accept decimal values (e.g., 4.5)
    
    **Popular Categories:**
    - **Theme Parks**: Disney World, Universal Studios, Six Flags
    - **Museums**: Art galleries, science museums, history museums
    - **Tours**: City tours, food tours, guided experiences
    - **Outdoor Activities**: Hiking, biking, water sports
    - **Cultural Experiences**: Local festivals, cultural shows
    """
    try:
        results = things_to_do_service.search_things_to_do(
            location=location,
            date=date,
            category=category,
            duration=duration,
            min_rating=min_rating,
            price_min=price_min,
            price_max=price_max
        )
        
        # Add imageUrl to each result
        for result in results:
            result["imageUrl"] = things_to_do_service._get_activity_image(
                result["id"], result["name"], result["category"]
            )
        
        if not results:
            raise HTTPException(
                status_code=404, 
                detail=f"No activities found for location '{location}' on {date}' with the specified filters."
            )
        
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/by-category",
    summary="Get Things to Do by Category",
    description="""
    Retrieve activities organized by category. This endpoint groups activities by their category
    and returns a structured response that makes it easy to browse activities by type.
    
    **Features:**
    - Get all activities organized by category
    - Filter by specific category if needed
    - Structured response with category groups
    - Includes pricing, ratings, and availability information
    - High-quality Unsplash images for each activity
    
    **Example Usage:**
    - Get all activities by category: `/by-category`
    - Get specific category: `/by-category?category=Theme Parks`
    - Get outdoor activities: `/by-category?category=Outdoor Activities`
    """,
    response_description="Activities organized by category",
    responses={
        200: {
            "description": "Successful response with activities grouped by category",
            "content": {
                "application/json": {
                    "example": [
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
                                    "originalPrice": None,
                                    "currency": "USD",
                                    "imageUrl": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=800&h=600&fit=crop",
                                    "tags": ["Skip-the-line", "Free cancellation"],
                                    "memberPrice": False
                                }
                            ]
                        }
                    ]
                }
            }
        },
        400: {"description": "Invalid category parameter"},
        404: {"description": "No activities found for the specified category"}
    }
)
async def get_things_to_do_by_category(
    category: Optional[str] = Query(
        None,
        description="Filter by specific category. If not provided, returns all categories.",
        example="Theme Parks",
        enum=["Theme Parks", "Museums", "Tours", "Outdoor Activities", "Cultural Experiences", "Adventure Sports", "Food & Dining", "Entertainment", "Shopping", "Wellness & Spa"]
    )
):
    """
    Get activities organized by category with optional filtering.
    
    **Parameters:**
    - `category` (optional): Filter by specific category. If not provided, returns all categories.
    
    **Response Structure:**
    - Returns an array of category objects
    - Each category contains an array of activity items
    - Items include pricing, ratings, duration, and availability information
    - High-quality Unsplash images for visual appeal
    
    **Available Categories:**
    - **Theme Parks**: Amusement parks and entertainment venues
    - **Museums**: Art galleries, science museums, history museums
    - **Tours**: Guided tours, city tours, food tours
    - **Outdoor Activities**: Hiking, biking, water sports, nature activities
    - **Cultural Experiences**: Local festivals, cultural shows, heritage sites
    - **Adventure Sports**: Extreme sports, adventure activities
    - **Food & Dining**: Food tours, cooking classes, dining experiences
    - **Entertainment**: Shows, concerts, nightlife
    - **Shopping**: Shopping tours, markets, retail experiences
    - **Wellness & Spa**: Spa treatments, wellness activities, relaxation
    
    **Use Cases:**
    - Browse activities by type for trip planning
    - Filter activities for specific interests
    - Compare activities within the same category
    - Discover new activity types in a destination
    """
    try:
        results = things_to_do_service.get_things_to_do_by_category(category)
        
        if not results:
            if category:
                raise HTTPException(
                    status_code=404,
                    detail=f"No activities found for category '{category}'."
                )
            else:
                raise HTTPException(
                    status_code=404,
                    detail="No activities found."
                )
        
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{thing_id}",
    summary="Get Activity Details",
    description="""
    Retrieve comprehensive information about a specific activity or attraction.
    
    **What You'll Get:**
    - Complete activity description and highlights
    - Pricing and availability information
    - What's included and not included
    - Important information and restrictions
    - Cancellation policies
    - Available time slots
    - High-quality activity image
    
    **Use Case:**
    After finding an activity through search, use this endpoint to get full details
    before making a booking decision.
    """,
    response_description="Detailed information about the requested activity",
    responses={
        200: {
            "description": "Activity details retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "ttd-1",
                        "name": "Universal Studios Hollywood Skip-the-Line Ticket",
                        "location": "Los Angeles, California",
                        "address": "100 Universal City Plaza, Universal City, CA 91608",
                        "category": "Theme Parks",
                        "price": 109.99,
                        "rating": 4.7,
                        "reviews_count": 2845,
                        "duration": "1 day",
                        "highlights": ["Skip-the-line admission", "Access to all rides"],
                        "description": "Skip the regular lines and head straight to the fun...",
                        "included": ["Skip-the-line park admission", "Access to all rides"],
                        "not_included": ["Food and drinks", "Parking fees"],
                        "important_info": ["Children aged 2 and under enter free"],
                        "available_times": ["09:00", "10:00", "11:00", "12:00"],
                        "cancellation_policy": {
                            "free_cancellation_before": "24h",
                            "refund_percentage": 100
                        },
                        "imageUrl": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=800&h=600&fit=crop"
                    }
                }
            }
        },
        404: {"description": "Activity not found"},
        400: {"description": "Invalid activity ID format"}
    }
)
async def get_thing_details(
    thing_id: str = Path(
        ..., 
        description="Unique identifier for the activity",
        example="ttd-1",
        regex="^ttd-\d+$"
    )
):
    """
    Get detailed information about a specific activity or attraction.
    
    **Parameters:**
    - `thing_id`: The unique identifier of the activity (format: ttd-{number})
    
    **Response Includes:**
    - **Basic Info**: Name, location, category, price, rating
    - **Details**: Full description, highlights, duration
    - **Practical Info**: Address, available times, what's included/excluded
    - **Policies**: Cancellation policy, important restrictions
    - **Reviews**: Rating and review count
    - **Image**: High-quality Unsplash image for the activity
    
    **Example IDs:**
    - `ttd-1`: Universal Studios Hollywood
    - `ttd-2`: Louvre Museum Tour
    - `ttd-3`: City Food Walking Tour
    
    **Error Handling:**
    - Returns 404 if the activity ID doesn't exist
    - Returns 400 if the ID format is invalid
    """
    try:
        details = things_to_do_service.get_thing_details(thing_id)
        
        if not details:
            raise HTTPException(
                status_code=404, 
                detail=f"Activity with ID '{thing_id}' not found. Please check the ID and try again."
            )
        
        # Add imageUrl to the details
        details["imageUrl"] = things_to_do_service._get_activity_image(
            details["id"], details["name"], details["category"]
        )
        
        return details
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
