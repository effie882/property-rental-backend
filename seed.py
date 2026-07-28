from datetime import date, datetime
from app import app, db, bcrypt
from models import User, Property, Booking, Payment, Review, Amenity, Favorite, MaintenanceRequest, PropertyImage


def seed_roles():
    roles = ["landlord", "tenant", "admin"]
    for role in roles:
        if not User.query.filter_by(role=role).first():
            user = User(
                first_name=role.capitalize(),
                last_name="User",
                email=f"{role}@rental.com",
                password_hash=bcrypt.generate_password_hash("password").decode("utf-8"),
                role=role,
                phone="+1234567890",
            )
            db.session.add(user)
    db.session.commit()


def seed_admin():
    if not User.query.filter_by(email="admin@rental.com").first():
        admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@rental.com",
            password_hash=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            role="admin",
            phone="+1234567890",
        )
        db.session.add(admin)
        db.session.commit()


def seed_amenities():
    amenities = [
        "WiFi", "Pool", "Parking", "Gym", "Air Conditioning",
        "Kitchen", "Washer", "Dryer", "TV", "Pet Friendly"
    ]
    for name in amenities:
        if not Amenity.query.filter_by(name=name).first():
            amenity = Amenity(name=name)
            db.session.add(amenity)
    db.session.commit()


def run_seeds():
    with app.app_context():
        db.create_all()
        seed_roles()
        seed_admin()
        seed_amenities()
        print("Database seeded successfully.")


if __name__ == "__main__":
    run_seeds()