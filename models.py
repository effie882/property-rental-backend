from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }

metadata = MetaData(naming_convention=naming_convention)

db = SQLAlchemy(metadata=metadata)


# Users

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    properties = db.relationship("Property", backref="landlord", lazy=True)
    bookings = db.relationship("Booking", backref="tenant", lazy=True)
    reviews = db.relationship("Review", backref="tenant", lazy=True)
    favorites = db.relationship("Favorite", backref="user", lazy=True)
    maintenance_requests = db.relationship(
        "MaintenanceRequest", backref="tenant", lazy=True
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"name='{self.first_name} {self.last_name}', "
            f"role='{self.role}')>"
        )

# Properties
class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    county = db.Column(db.String(100))
    property_type = db.Column(db.String(50))
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("Booking", backref="property", lazy=True)
    reviews = db.relationship("Review", backref="property", lazy=True)
    favorites = db.relationship("Favorite", backref="property", lazy=True)
    maintenance_requests = db.relationship(
        "MaintenanceRequest",
        backref="property",
        lazy=True
    )
    images = db.relationship("PropertyImage", backref="property", lazy=True)

    amenities = db.relationship(
        "Amenity",
        secondary="property_amenities",
        back_populates="properties"
    )

# Bookings
class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    tenant_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)

    total_amount = db.Column(db.Numeric(10, 2))
    booking_status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    payment = db.relationship(
        "Payment",
        backref="booking",
        uselist=False
    )

# Payments
class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    booking_id = db.Column(
        db.Integer,
        db.ForeignKey("bookings.id"),
        nullable=False
    )

    amount = db.Column(db.Numeric(10, 2))
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    payment_date = db.Column(db.DateTime)

    # Reviews
class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    tenant_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Favorites
class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Maintenance Requests
class MaintenanceRequest(db.Model):
    __tablename__ = "maintenance_requests"

    id = db.Column(db.Integer, primary_key=True)

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    tenant_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    issue = db.Column(db.Text)
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Property Images
class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id = db.Column(db.Integer, primary_key=True)

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    image_url = db.Column(db.String(255))

    # Amenities
class Amenity(db.Model):
    __tablename__ = "amenities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    properties = db.relationship(
        "Property",
        secondary="property_amenities",
        back_populates="amenities"
    )
    
# Association Table
property_amenities = db.Table(
    "property_amenities",

    db.Column(
        "property_id",
        db.Integer,
        db.ForeignKey("properties.id"),
        primary_key=True
    ),

    db.Column(
        "amenity_id",
        db.Integer,
        db.ForeignKey("amenities.id"),
        primary_key=True
    )
)
