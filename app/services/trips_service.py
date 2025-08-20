import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

class TripsService:
    def plan_trip(self, db, payload):
        from app.db import models
        user = db.query(models.User).filter(models.User.email == payload.email).first()
        if not user:
            raise Exception("User not found")
        trip = models.UserTrip(
            user_id=user.id,
            trip_id=payload.trip_id,
            trip_name=payload.trip_name,
            destination=payload.destination,
            start_date=payload.start_date,
            end_date=payload.end_date,
            trip_type=payload.trip_type,
            invite_flag=payload.invite_flag,
            created_for_you=payload.created_for_you,
            notes=payload.notes
        )
        db.add(trip)
        db.commit()
        db.refresh(trip)
        return trip

    def list_user_trips(self, db, email):
        from app.db import models
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            return []
        trips = db.query(models.UserTrip).filter(models.UserTrip.user_id == user.id).all()
        return trips

    def remove_user_trip(self, db, email, trip_id):
        from app.db import models
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise Exception("User not found")
        trip = db.query(models.UserTrip).filter(models.UserTrip.user_id == user.id, models.UserTrip.id == trip_id).first()
        if not trip:
            raise Exception("Trip not found")
        db.delete(trip)
        db.commit()
        return True
    def _load(self, name: str):
        with open(DATA_DIR / f"{name}.json", encoding="utf-8") as f:
            return json.load(f)

    def get_trips(self):
        return self._load("trips_list")