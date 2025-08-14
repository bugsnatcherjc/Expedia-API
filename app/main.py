from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import home, stays, flights, cars, activities, trips, checkout, auth, packages, meta_ui, cruises, things_to_do, bookings
from app.db.database import Base, engine, SessionLocal
from app.db import models

app = FastAPI(title="Expedia Inspired API", version="1.0.0")
Base.metadata.create_all(bind=engine)
def seed_data():
    db = SessionLocal()
    try:
        # Check if test user exists
        if not db.query(models.User).filter(models.User.email == "test@example.com").first():
            user = models.User(
                username="testuser",
                email="test@example.com",
                password="password123"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            # Add a booking for the test user
            booking = models.Booking(
                booking_type="flight",
                item_id=101,
                details="Test flight from NYC to LA",
                price=299.99,
                user_id=user.id
            )
            db.add(booking)
            db.commit()

            print("✅ Seed data created: test user & booking")
        else:
            print("ℹ️ Seed data already exists, skipping...")
    finally:
        db.close()

seed_data()
app.add_middleware(
    CORSMiddleware,
    # TODO: need to change this to a specific domain in production
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(home.router)
app.include_router(stays.router)
app.include_router(flights.router)
app.include_router(cars.router)
app.include_router(activities.router)
app.include_router(bookings.router)
app.include_router(cruises.router)
app.include_router(things_to_do.router)
app.include_router(trips.router)
app.include_router(packages.router)
app.include_router(checkout.router)
app.include_router(auth.router)
app.include_router(meta_ui.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Expedia Inspired API"}