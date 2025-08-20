from app.db.database import SessionLocal
from app.db import models

def seed_data():
    db = SessionLocal()
    try:
        # Check if test user exists
        if not db.query(models.User).filter(models.User.email == "test@example.com").first():
            user = models.User(
                username="testuser",
                email="test@example.com",
                password="password123",
                phone="+1234567890",
                is_verified=True
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
            print("📧 OTP System: Static OTP = 123456 (for development)")
        else:
            print("ℹ️ Seed data already exists, skipping...")
            print("📧 OTP System: Static OTP = 123456 (for development)")
    except Exception as e:
        print("🔄 Database schema mismatch detected. Please delete expedia_inspired.db and restart.")
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
