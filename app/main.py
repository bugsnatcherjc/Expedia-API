from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import stays, flights, cars, activities, trips, checkout, auth, packages, meta_ui, cruises, things_to_do, bookings
from app.db.database import Base, engine
from app.db.migrations import ensure_sqlite_columns
from app.core.config import settings, print_startup_config
from app.seed import seed_data  # move seeding into separate file ideally

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

# DB setup
Base.metadata.create_all(bind=engine)
try:
    ensure_sqlite_columns(engine)
except Exception as e:
    print(f"⚠️ SQLite auto-migration warning: {e}")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
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

# Root
@app.get("/")
async def root():
    return {"message": "Welcome to Expedia Inspired API"}

# Health check
@app.get("/healthz")
async def health():
    return {"status": "healthy"}

# Startup tasks
@app.on_event("startup")
def startup_event():
    seed_data()
    print("✅ Startup tasks complete")
