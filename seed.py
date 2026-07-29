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


def seed_properties():
    landlord = User.query.filter_by(role="landlord").first()
    if not landlord:
        return
    if Property.query.filter_by(title="Sunny Apartment").first():
        return

    amenities = {name: Amenity.query.filter_by(name=name).first() for name in [
        "WiFi", "Pool", "Parking", "Gym", "Air Conditioning", "Kitchen"
    ]}

    properties_data = [
        {
            "landlord_id": landlord.id,
            "title": "Sunny Apartment",
            "description": "A bright and spacious apartment in the city center.",
            "address": "123 Main St",
            "city": "Nairobi",
            "county": "Nairobi",
            "property_type": "Apartment",
            "bedrooms": 2,
            "bathrooms": 1,
            "price": 800.00,
            "status": "available",
            "image_url": "https://example.com/sunny-apartment.jpg",
            "amenity_names": ["WiFi", "Pool", "Parking"],
        },
        {
            "landlord_id": landlord.id,
            "title": "Cozy Studio",
            "description": "A comfortable studio close to the university.",
            "address": "456 University Ave",
            "city": "Nairobi",
            "county": "Nairobi",
            "property_type": "Studio",
            "bedrooms": 1,
            "bathrooms": 1,
            "price": 450.00,
            "status": "available",
            "image_url": "https://example.com/cozy-studio.jpg",
            "amenity_names": ["WiFi", "Kitchen", "TV"],
        },
        {
            "landlord_id": landlord.id,
            "title": "Luxury Villa",
            "description": "A premium villa with pool and garden.",
            "address": "789 Hillside Dr",
            "city": "Nairobi",
            "county": "Nairobi",
            "property_type": "Villa",
            "bedrooms": 4,
            "bathrooms": 3,
            "price": 2500.00,
            "status": "available",
            "image_url": "https://example.com/luxury-villa.jpg",
            "amenity_names": ["WiFi", "Pool", "Parking", "Gym", "Air Conditioning", "Kitchen", "Washer", "Dryer", "TV", "Pet Friendly"],
        },
    ]

    for pdata in properties_data:
        amenity_names = pdata.pop("amenity_names")
        prop = Property(**pdata)
        db.session.add(prop)
        db.session.flush()
        for name in amenity_names:
            amenity = amenities.get(name)
            if amenity:
                prop.amenities.append(amenity)

    db.session.commit()


def seed_bookings():
    tenant = User.query.filter_by(role="tenant").first()
    landlord = User.query.filter_by(role="landlord").first()
    if not tenant or not landlord:
        return

    if Booking.query.first():
        return

    prop1 = Property.query.filter_by(title="Sunny Apartment").first()
    prop2 = Property.query.filter_by(title="Cozy Studio").first()
    if not prop1 or not prop2:
        return

    bookings_data = [
        {
            "property_id": prop1.id,
            "tenant_id": tenant.id,
            "check_in": date(2026, 8, 1),
            "check_out": date(2026, 8, 7),
            "total_amount": 4800.00,
            "booking_status": "confirmed",
        },
        {
            "property_id": prop2.id,
            "tenant_id": tenant.id,
            "check_in": date(2026, 9, 15),
            "check_out": date(2026, 9, 20),
            "total_amount": 2250.00,
            "booking_status": "pending",
        },
    ]

    for bdata in bookings_data:
        booking = Booking(**bdata)
        db.session.add(booking)

    db.session.commit()


def seed_payments():
    if Payment.query.first():
        return

    bookings = Booking.query.all()
    if not bookings:
        return

    payments_data = [
        {
            "booking_id": bookings[0].id,
            "amount": 4800.00,
            "payment_method": "credit_card",
            "payment_status": "completed",
            "transaction_id": "txn_001",
            "payment_date": datetime(2026, 7, 28, 10, 0, 0),
        },
        {
            "booking_id": bookings[1].id,
            "amount": 2250.00,
            "payment_method": "bank_transfer",
            "payment_status": "pending",
            "transaction_id": "txn_002",
            "payment_date": datetime(2026, 7, 28, 11, 0, 0),
        },
    ]

    for pdata in payments_data:
        payment = Payment(**pdata)
        db.session.add(payment)

    db.session.commit()


def seed_reviews():
    tenant = User.query.filter_by(role="tenant").first()
    prop1 = Property.query.filter_by(title="Sunny Apartment").first()
    if not tenant or not prop1:
        return
    if Review.query.first():
        return

    reviews_data = [
        {
            "property_id": prop1.id,
            "tenant_id": tenant.id,
            "rating": 5,
            "comment": "Great place, very clean and spacious!",
            "created_at": datetime(2026, 8, 8, 0, 0, 0),
        },
    ]

    for rdata in reviews_data:
        review = Review(**rdata)
        db.session.add(review)

    db.session.commit()


def seed_favorites():
    tenant = User.query.filter_by(role="tenant").first()
    prop1 = Property.query.filter_by(title="Sunny Apartment").first()
    prop2 = Property.query.filter_by(title="Luxury Villa").first()
    if not tenant or not prop1 or not prop2:
        return
    if Favorite.query.first():
        return

    fav1 = Favorite(user_id=tenant.id, property_id=prop1.id)
    fav2 = Favorite(user_id=tenant.id, property_id=prop2.id)
    db.session.add(fav1)
    db.session.add(fav2)

    db.session.commit()


def seed_maintenance_requests():
    tenant = User.query.filter_by(role="tenant").first()
    prop1 = Property.query.filter_by(title="Sunny Apartment").first()
    if not tenant or not prop1:
        return
    if MaintenanceRequest.query.first():
        return

    mr = MaintenanceRequest(
        property_id=prop1.id,
        tenant_id=tenant.id,
        issue="Leaky faucet in the kitchen",
        status="open",
    )
    db.session.add(mr)

    db.session.commit()


def seed_property_images():
    prop1 = Property.query.filter_by(title="Sunny Apartment").first()
    prop2 = Property.query.filter_by(title="Cozy Studio").first()
    prop3 = Property.query.filter_by(title="Luxury Villa").first()
    if not prop1 or not prop2 or not prop3:
        return
    if PropertyImage.query.first():
        return

    images_data = [
        {"property_id": prop1.id, "image_url": "https://example.com/sunny-1.jpg"},
        {"property_id": prop1.id, "image_url": "https://example.com/sunny-2.jpg"},
        {"property_id": prop2.id, "image_url": "https://example.com/studio-1.jpg"},
        {"property_id": prop3.id, "image_url": "https://example.com/villa-1.jpg"},
        {"property_id": prop3.id, "image_url": "https://example.com/villa-2.jpg"},
    ]

    for idata in images_data:
        img = PropertyImage(**idata)
        db.session.add(img)

    db.session.commit()


def run_seeds():
    with app.app_context():
        db.create_all()
        seed_roles()
        seed_admin()
        seed_amenities()
        seed_properties()
        seed_bookings()
        seed_payments()
        seed_reviews()
        seed_favorites()
        seed_maintenance_requests()
        seed_property_images()
        print("Database seeded successfully.")


if __name__ == "__main__":
    run_seeds()