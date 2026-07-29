from datetime import date, datetime
from app import app, db, bcrypt
from sqlalchemy import select, func
from models import (
    User,
    Property,
    Booking,
    Payment,
    Review,
    Favorite,
    MaintenanceRequest,
    PropertyImage,
    Amenity,
)
from models import property_amenities


def hash_pw(raw):
    return bcrypt.generate_password_hash(raw).decode("utf-8")


def seed_users():
    print("Seeding users...")
    users = [
        User(first_name="John", last_name="Kamau", email="john@example.com",
             password_hash=hash_pw("password123"), phone="0712345678", role="landlord"),
        User(first_name="Jane", last_name="Wanjiku", email="jane@example.com",
             password_hash=hash_pw("password123"), phone="0712000002", role="landlord"),
        User(first_name="Mary", last_name="Achieng", email="mary@example.com",
             password_hash=hash_pw("password123"), phone="0798765432", role="tenant"),
        User(first_name="Brian", last_name="Mwangi", email="brian@example.com",
             password_hash=hash_pw("password123"), phone="0798000002", role="tenant"),
        User(first_name="Alex", last_name="Otieno", email="alex@example.com",
             password_hash=hash_pw("password123"), phone="0798000003", role="tenant"),
        User(first_name="Admin", last_name="User", email="admin@example.com",
             password_hash=hash_pw("password123"), phone="0700000000", role="admin"),
    ]
    db.session.add_all(users)
    db.session.commit()


def seed_amenities():
    print("Seeding amenities...")
    amenities = [
        Amenity(name="WiFi"),
        Amenity(name="Parking"),
        Amenity(name="Pool"),
        Amenity(name="Kitchen"),
        Amenity(name="Air Conditioning"),
        Amenity(name="Security"),
        Amenity(name="Generator"),
    ]
    db.session.add_all(amenities)
    db.session.commit()
    return {a.name: a for a in amenities}


def seed_properties(amenities_map):
    print("Seeding properties...")
    john = User.query.filter_by(email="john@example.com").first()
    jane = User.query.filter_by(email="jane@example.com").first()

    p1 = Property(landlord_id=john.id, title="Modern Apartment",
                  description="Beautiful 2-bedroom apartment.",
                  address="Ngong Road", city="Nairobi", county="Nairobi",
                  property_type="Apartment", bedrooms=2, bathrooms=2, price=3500,
                  status="available", image_url="https://example.com/apartment.jpg")
    p2 = Property(landlord_id=john.id, title="City Studio",
                  description="Compact studio close to the CBD.",
                  address="Kimathi Street", city="Nairobi", county="Nairobi",
                  property_type="Studio", bedrooms=1, bathrooms=1, price=2200,
                  status="available", image_url="https://example.com/studio.jpg")
    p3 = Property(landlord_id=jane.id, title="Ocean View Villa",
                  description="Spacious villa with sea views.",
                  address="Nyali Road", city="Mombasa", county="Mombasa",
                  property_type="Villa", bedrooms=4, bathrooms=3, price=9500,
                  status="available", image_url="https://example.com/villa.jpg")
    p4 = Property(landlord_id=jane.id, title="Lakeside Cottage",
                  description="Cozy cottage on the lake shore.",
                  address="Moi South Lake Road", city="Naivasha", county="Nakuru",
                  property_type="Cottage", bedrooms=2, bathrooms=1, price=4800,
                  status="booked", image_url="https://example.com/cottage.jpg")
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()
    return {"p1": p1, "p2": p2, "p3": p3, "p4": p4}


def seed_property_amenities(properties_map, amenities_map):
    print("Seeding property amenities...")
    p1 = properties_map["p1"]
    p2 = properties_map["p2"]
    p3 = properties_map["p3"]
    p4 = properties_map["p4"]
    rows = [
        (p1.id, amenities_map["WiFi"].id),
        (p1.id, amenities_map["Parking"].id),
        (p1.id, amenities_map["Kitchen"].id),
        (p2.id, amenities_map["WiFi"].id),
        (p2.id, amenities_map["Security"].id),
        (p3.id, amenities_map["WiFi"].id),
        (p3.id, amenities_map["Pool"].id),
        (p3.id, amenities_map["Air Conditioning"].id),
        (p3.id, amenities_map["Generator"].id),
        (p4.id, amenities_map["Kitchen"].id),
        (p4.id, amenities_map["Parking"].id),
    ]
    for prop_id, amenity_id in rows:
        db.session.execute(property_amenities.insert().values(property_id=prop_id, amenity_id=amenity_id))
    db.session.commit()


def seed_property_images(properties_map):
    print("Seeding property images...")
    p1 = properties_map["p1"]
    p2 = properties_map["p2"]
    p3 = properties_map["p3"]
    p4 = properties_map["p4"]
    images = [
        PropertyImage(property_id=p1.id, image_url="https://example.com/property1-a.jpg"),
        PropertyImage(property_id=p1.id, image_url="https://example.com/property1-b.jpg"),
        PropertyImage(property_id=p2.id, image_url="https://example.com/property2-a.jpg"),
        PropertyImage(property_id=p3.id, image_url="https://example.com/property3-a.jpg"),
        PropertyImage(property_id=p3.id, image_url="https://example.com/property3-b.jpg"),
        PropertyImage(property_id=p4.id, image_url="https://example.com/property4-a.jpg"),
    ]
    db.session.add_all(images)
    db.session.commit()


def seed_bookings(properties_map):
    print("Seeding bookings...")
    mary = User.query.filter_by(email="mary@example.com").first()
    brian = User.query.filter_by(email="brian@example.com").first()
    alex = User.query.filter_by(email="alex@example.com").first()
    p1 = properties_map["p1"]
    p2 = properties_map["p2"]
    p3 = properties_map["p3"]
    p4 = properties_map["p4"]
    bookings = [
        Booking(property_id=p1.id, tenant_id=mary.id,
                check_in=date(2026, 8, 1), check_out=date(2026, 8, 5),
                total_amount=14000, booking_status="confirmed"),
        Booking(property_id=p3.id, tenant_id=brian.id,
                check_in=date(2026, 9, 10), check_out=date(2026, 9, 15),
                total_amount=47500, booking_status="confirmed"),
        Booking(property_id=p4.id, tenant_id=alex.id,
                check_in=date(2026, 6, 1), check_out=date(2026, 6, 4),
                total_amount=14400, booking_status="completed"),
        Booking(property_id=p2.id, tenant_id=mary.id,
                check_in=date(2026, 10, 1), check_out=date(2026, 10, 3),
                total_amount=4400, booking_status="cancelled"),
    ]
    db.session.add_all(bookings)
    db.session.commit()
    return bookings


def seed_payments(bookings):
    print("Seeding payments...")
    payments = [
        Payment(booking_id=bookings[0].id, amount=14000, payment_method="M-Pesa",
                payment_status="completed", transaction_id="TXN100001"),
        Payment(booking_id=bookings[1].id, amount=47500, payment_method="M-Pesa",
                payment_status="completed", transaction_id="TXN100002"),
        Payment(booking_id=bookings[2].id, amount=14400, payment_method="Card",
                payment_status="completed", transaction_id="TXN100003"),
    ]
    db.session.add_all(payments)
    db.session.commit()


def seed_reviews(properties_map):
    print("Seeding reviews...")
    mary = User.query.filter_by(email="mary@example.com").first()
    brian = User.query.filter_by(email="brian@example.com").first()
    alex = User.query.filter_by(email="alex@example.com").first()
    p1 = properties_map["p1"]
    p3 = properties_map["p3"]
    p4 = properties_map["p4"]
    reviews = [
        Review(property_id=p1.id, tenant_id=mary.id, rating=5, comment="Excellent place!"),
        Review(property_id=p3.id, tenant_id=brian.id, rating=4, comment="Lovely villa, great views."),
        Review(property_id=p4.id, tenant_id=alex.id, rating=5, comment="Peaceful and clean."),
    ]
    db.session.add_all(reviews)
    db.session.commit()


def seed_favorites(properties_map):
    print("Seeding favorites...")
    mary = User.query.filter_by(email="mary@example.com").first()
    brian = User.query.filter_by(email="brian@example.com").first()
    alex = User.query.filter_by(email="alex@example.com").first()
    p1 = properties_map["p1"]
    p2 = properties_map["p2"]
    p3 = properties_map["p3"]
    favorites = [
        Favorite(user_id=mary.id, property_id=p3.id),
        Favorite(user_id=brian.id, property_id=p1.id),
        Favorite(user_id=alex.id, property_id=p2.id),
        Favorite(user_id=alex.id, property_id=p3.id),
    ]
    db.session.add_all(favorites)
    db.session.commit()


def seed_maintenance_requests(properties_map):
    print("Seeding maintenance requests...")
    mary = User.query.filter_by(email="mary@example.com").first()
    brian = User.query.filter_by(email="brian@example.com").first()
    alex = User.query.filter_by(email="alex@example.com").first()
    p1 = properties_map["p1"]
    p3 = properties_map["p3"]
    p4 = properties_map["p4"]
    requests = [
        MaintenanceRequest(property_id=p1.id, tenant_id=mary.id,
                           issue="Leaking kitchen sink", status="pending"),
        MaintenanceRequest(property_id=p3.id, tenant_id=brian.id,
                           issue="Air conditioning not cooling", status="in_progress"),
        MaintenanceRequest(property_id=p4.id, tenant_id=alex.id,
                           issue="Broken window latch", status="resolved"),
    ]
    db.session.add_all(requests)
    db.session.commit()


def run_seeds():
    with app.app_context():
        db.create_all()

        for model in [Payment, Review, Favorite, MaintenanceRequest, PropertyImage,
                      Booking, Property, Amenity, User]:
            model.query.delete()
        db.session.commit()

        amenities_map = seed_amenities()
        seed_users()
        properties_map = seed_properties(amenities_map)
        seed_property_amenities(properties_map, amenities_map)
        seed_property_images(properties_map)
        bookings = seed_bookings(properties_map)
        seed_payments(bookings)
        seed_reviews(properties_map)
        seed_favorites(properties_map)
        seed_maintenance_requests(properties_map)

        print("\nDatabase seeded successfully!")
        print(f"   Users:                {User.query.count()}")
        print(f"   Properties:           {Property.query.count()}")
        print(f"   Amenities:            {Amenity.query.count()}")
        print(f"   Property Amenities:   {db.session.execute(select(func.count()).select_from(property_amenities)).scalar()}")
        print(f"   Property Images:      {PropertyImage.query.count()}")
        print(f"   Bookings:             {Booking.query.count()}")
        print(f"   Payments:             {Payment.query.count()}")
        print(f"   Reviews:              {Review.query.count()}")
        print(f"   Favorites:            {Favorite.query.count()}")
        print(f"   Maintenance Requests: {MaintenanceRequest.query.count()}")
        print("\nLogin credentials (all passwords: password123):")
        print("   Landlord -> john@example.com")
        print("   Landlord -> jane@example.com")
        print("   Tenant   -> mary@example.com")
        print("   Tenant   -> brian@example.com")
        print("   Tenant   -> alex@example.com")
        print("   Admin    -> admin@example.com")


if __name__ == "__main__":
    run_seeds()