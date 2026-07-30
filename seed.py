from app import app, bcrypt
from models import (
    db,
    User,
    Property,
    Booking,
    Payment,
    Review,
    Favorite,
    MaintenanceRequest,
    PropertyImage,
    Amenity,
    PropertyAmenity
)

from datetime import date


with app.app_context():

    print("Deleting old data...")

    PropertyAmenity.query.delete()
    PropertyImage.query.delete()
    MaintenanceRequest.query.delete()
    Favorite.query.delete()
    Review.query.delete()
    Payment.query.delete()
    Booking.query.delete()
    Property.query.delete()
    Amenity.query.delete()
    User.query.delete()
    db.session.commit()

    def hash_pw(raw):
        return bcrypt.generate_password_hash(raw).decode("utf-8")

    # =========================================================================
    # USERS — 2 landlords, 3 tenants, 1 admin
    # =========================================================================
    print("Seeding users...")

    john = User(first_name="John", last_name="Kamau", email="john@example.com",
                password_hash=hash_pw("password123"), phone="0712345678", role="landlord")
    jane = User(first_name="Jane", last_name="Wanjiku", email="jane@example.com",
                password_hash=hash_pw("password123"), phone="0712000002", role="landlord")
    mary = User(first_name="Mary", last_name="Achieng", email="mary@example.com",
                password_hash=hash_pw("password123"), phone="0798765432", role="tenant")
    brian = User(first_name="Brian", last_name="Mwangi", email="brian@example.com",
                 password_hash=hash_pw("password123"), phone="0798000002", role="tenant")
    alex = User(first_name="Alex", last_name="Otieno", email="alex@example.com",
                password_hash=hash_pw("password123"), phone="0798000003", role="tenant")
    admin = User(first_name="Admin", last_name="User", email="admin@example.com",
                 password_hash=hash_pw("password123"), phone="0700000000", role="admin")

    db.session.add_all([john, jane, mary, brian, alex, admin])
    db.session.commit()

    # =========================================================================
    # AMENITIES — created once, reused across properties
    # =========================================================================
    print("Seeding amenities...")

    wifi        = Amenity(name="WiFi")
    parking     = Amenity(name="Parking")
    pool        = Amenity(name="Pool")
    kitchen     = Amenity(name="Kitchen")
    ac          = Amenity(name="Air Conditioning")
    security    = Amenity(name="Security")
    generator   = Amenity(name="Generator")

    db.session.add_all([wifi, parking, pool, kitchen, ac, security, generator])
    db.session.commit()

    # =========================================================================
    # PROPERTIES — 4 properties across 2 landlords
    # =========================================================================
    print("Seeding properties...")

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

    # =========================================================================
    # PROPERTY_AMENITIES (junction) — every property gets amenities
    # =========================================================================
    print("Seeding property amenities...")

    db.session.add_all([
        PropertyAmenity(property_id=p1.id, amenity_id=wifi.id),
        PropertyAmenity(property_id=p1.id, amenity_id=parking.id),
        PropertyAmenity(property_id=p1.id, amenity_id=kitchen.id),

        PropertyAmenity(property_id=p2.id, amenity_id=wifi.id),
        PropertyAmenity(property_id=p2.id, amenity_id=security.id),

        PropertyAmenity(property_id=p3.id, amenity_id=wifi.id),
        PropertyAmenity(property_id=p3.id, amenity_id=pool.id),
        PropertyAmenity(property_id=p3.id, amenity_id=ac.id),
        PropertyAmenity(property_id=p3.id, amenity_id=generator.id),

        PropertyAmenity(property_id=p4.id, amenity_id=kitchen.id),
        PropertyAmenity(property_id=p4.id, amenity_id=parking.id),
    ])
    db.session.commit()

    # =========================================================================
    # PROPERTY_IMAGES — extra gallery shots for each property
    # =========================================================================
    print("Seeding property images...")

    db.session.add_all([
        PropertyImage(property_id=p1.id, image_url="https://example.com/property1-a.jpg"),
        PropertyImage(property_id=p1.id, image_url="https://example.com/property1-b.jpg"),
        PropertyImage(property_id=p2.id, image_url="https://example.com/property2-a.jpg"),
        PropertyImage(property_id=p3.id, image_url="https://example.com/property3-a.jpg"),
        PropertyImage(property_id=p3.id, image_url="https://example.com/property3-b.jpg"),
        PropertyImage(property_id=p4.id, image_url="https://example.com/property4-a.jpg"),
    ])
    db.session.commit()

    # =========================================================================
    # BOOKINGS — spread across tenants and properties
    # =========================================================================
    print("Seeding bookings...")

    b1 = Booking(property_id=p1.id, tenant_id=mary.id,
                 check_in=date(2026, 8, 1), check_out=date(2026, 8, 5),
                 total_amount=14000, booking_status="confirmed")

    b2 = Booking(property_id=p3.id, tenant_id=brian.id,
                 check_in=date(2026, 9, 10), check_out=date(2026, 9, 15),
                 total_amount=47500, booking_status="confirmed")

    b3 = Booking(property_id=p4.id, tenant_id=alex.id,
                 check_in=date(2026, 6, 1), check_out=date(2026, 6, 4),
                 total_amount=14400, booking_status="completed")

    b4 = Booking(property_id=p2.id, tenant_id=mary.id,
                 check_in=date(2026, 10, 1), check_out=date(2026, 10, 3),
                 total_amount=4400, booking_status="cancelled")

    db.session.add_all([b1, b2, b3, b4])
    db.session.commit()

    # =========================================================================
    # PAYMENTS — one per confirmed/completed booking (one-to-one)
    # =========================================================================
    print("Seeding payments...")

    db.session.add_all([
        Payment(booking_id=b1.id, amount=14000, payment_method="M-Pesa",
                payment_status="completed", transaction_id="TXN100001"),
        Payment(booking_id=b2.id, amount=47500, payment_method="M-Pesa",
                payment_status="completed", transaction_id="TXN100002"),
        Payment(booking_id=b3.id, amount=14400, payment_method="Card",
                payment_status="completed", transaction_id="TXN100003"),
        # b4 was cancelled before payment, so it intentionally has none —
        # demonstrates a booking WITHOUT a payment.
    ])
    db.session.commit()

    # =========================================================================
    # REVIEWS — from tenants who completed stays
    # =========================================================================
    print("Seeding reviews...")

    db.session.add_all([
        Review(property_id=p1.id, tenant_id=mary.id, rating=5, comment="Excellent place!"),
        Review(property_id=p3.id, tenant_id=brian.id, rating=4, comment="Lovely villa, great views."),
        Review(property_id=p4.id, tenant_id=alex.id, rating=5, comment="Peaceful and clean."),
    ])
    db.session.commit()

    # =========================================================================
    # FAVORITES — tenants saving properties they like
    # =========================================================================
    print("Seeding favorites...")

    db.session.add_all([
        Favorite(user_id=mary.id, property_id=p3.id),
        Favorite(user_id=brian.id, property_id=p1.id),
        Favorite(user_id=alex.id, property_id=p2.id),
        Favorite(user_id=alex.id, property_id=p3.id),
    ])
    db.session.commit()

    # =========================================================================
    # MAINTENANCE REQUESTS — a mix of statuses
    # =========================================================================
    print("Seeding maintenance requests...")

    db.session.add_all([
        MaintenanceRequest(property_id=p1.id, tenant_id=mary.id,
                           issue="Leaking kitchen sink", status="pending"),
        MaintenanceRequest(property_id=p3.id, tenant_id=brian.id,
                           issue="Air conditioning not cooling", status="in_progress"),
        MaintenanceRequest(property_id=p4.id, tenant_id=alex.id,
                           issue="Broken window latch", status="resolved"),
    ])
    db.session.commit()

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\nDatabase seeded successfully!\n")
    print(f"   Users:                {User.query.count()}")
    print(f"   Properties:           {Property.query.count()}")
    print(f"   Amenities:            {Amenity.query.count()}")
    print(f"   Property Amenities:   {PropertyAmenity.query.count()}")
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