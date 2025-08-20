from app.db.database import SessionLocal
from app.db import models

def seed_data():
    db = SessionLocal()
    try:
        # Always ensure test user exists
        user = db.query(models.User).filter(models.User.email == "user@example.com").first()
        if not user:
            user = models.User(
                username="testuser",
                email="user@example.com",
                password="password123",
                phone="+1234567890",
                is_verified=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Remove existing payment methods for user
        from app.db.models import PaymentMethod
        db.query(PaymentMethod).filter(PaymentMethod.user_id == user.id).delete()
        db.commit()

        # Seed payment methods for test user
        payment_methods = [
            {
                "card_type": "Visa",
                "cardholder": "User Example",
                "last4": "1234",
                "exp_month": "08",
                "exp_year": "2028",
                "csc": "321",
                "billing_address": "123 Main St, NY"
            },
            {
                "card_type": "Mastercard",
                "cardholder": "User Example",
                "last4": "5678",
                "exp_month": "11",
                "exp_year": "2027",
                "csc": "654",
                "billing_address": "456 Elm St, CA"
            }
        ]
        for pm in payment_methods:
            payment = PaymentMethod(
                user_id=user.id,
                card_type=pm["card_type"],
                cardholder=pm["cardholder"],
                last4=pm["last4"],
                exp_month=pm["exp_month"],
                exp_year=pm["exp_year"],
                csc=pm["csc"],
                billing_address=pm["billing_address"]
            )
            db.add(payment)
        db.commit()

        # Remove existing trips for user
        from app.db.models import UserTrip
        db.query(UserTrip).filter(UserTrip.user_id == user.id).delete()
        db.commit()

        # Seed planned trips for test user
        trips = [
            {
                "trip_id": 1,
                "trip_name": "Paris Romantic Getaway",
                "destination": "Paris",
                "start_date": "2025-09-01",
                "end_date": "2025-09-10",
                "trip_type": "flight",
                "invite_flag": False,
                "created_for_you": False,
                "notes": "Guided tours and gourmet dining.",
                "image": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
                "status": "past"
            },
            {
                "trip_id": 2,
                "trip_name": "Tokyo Explorer",
                "destination": "Tokyo",
                "start_date": "2025-10-15",
                "end_date": "2025-10-22",
                "trip_type": "flight",
                "invite_flag": True,
                "created_for_you": False,
                "notes": "Vibrant culture and cuisine.",
                "image": "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=800&q=80",
                "status": "canceled"
            },
            {
                "trip_id": 3,
                "trip_name": "New York Broadway",
                "destination": "New York",
                "start_date": "2025-11-05",
                "end_date": "2025-11-12",
                "trip_type": "hotel",
                "invite_flag": False,
                "created_for_you": False,
                "notes": "Broadway, museums, and shopping.",
                "image": "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=800&q=80",
                "status": "current"
            },
            {
                "trip_id": 4,
                "trip_name": "Sydney Adventure",
                "destination": "Sydney",
                "start_date": "2025-12-01",
                "end_date": "2025-12-10",
                "trip_type": "hotel",
                "invite_flag": False,
                "created_for_you": True,
                "notes": "Beaches and Opera House.",
                "image": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=800&q=80",
                "status": "current"
            }
        ]
        for t in trips:
            user_trip = UserTrip(
                user_id=user.id,
                trip_id=t["trip_id"],
                trip_name=t["trip_name"],
                destination=t["destination"],
                start_date=t["start_date"],
                end_date=t["end_date"],
                trip_type=t["trip_type"],
                invite_flag=t["invite_flag"],
                created_for_you=t["created_for_you"],
                notes=t["notes"],
                image=t.get("image"),
                status=t["status"]
            )
            db.add(user_trip)
        db.commit()
        print("✅ Seed data created: test user, payment methods, and planned trips reseeded")
        print("📧 OTP System: Static OTP = 123456 (for development)")
    # ...existing code...
    except Exception as e:
        print("🔄 Database schema mismatch detected. Please delete expedia_inspired.db and restart.")
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
