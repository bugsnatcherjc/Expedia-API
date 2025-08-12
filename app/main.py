from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import home, stays, flights, cars, activities, trips, checkout, auth

app = FastAPI(title="Expedia Inspired API", version="1.0.0")

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
app.include_router(trips.router)
app.include_router(checkout.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Expedia Inspired API"}