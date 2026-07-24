from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime


naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)

db = SQLAlchemy(metadata=metadata)


# =====================================================
# ASSOCIATION TABLE
# =====================================================

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


# =====================================================
# USER
# =====================================================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    phone = db.Column(db.String(20))

    role = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # One landlord has many properties
    properties = db.relationship(
        "Property",
        back_populates="landlord",
        lazy=True
    )

    # One tenant has many bookings
    bookings = db.relationship(
        "Booking",
        back_populates="tenant",
        lazy=True
    )

    # One tenant has many reviews
    reviews = db.relationship(
        "Review",
        back_populates="tenant",
        lazy=True
    )

    # One user has many favorites
    favorites = db.relationship(
        "Favorite",
        back_populates="user",
        lazy=True
    )

    # One tenant has many maintenance requests
    maintenance_requests = db.relationship(
        "MaintenanceRequest",
        back_populates="tenant",
        lazy=True
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"name='{self.first_name} {self.last_name}', "
            f"role='{self.role}')>"
        )


# =====================================================
# PROPERTY
# =====================================================

class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    landlord_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(db.Text)

    address = db.Column(db.String(255))

    city = db.Column(db.String(100))

    county = db.Column(db.String(100))

    property_type = db.Column(db.String(50))

    bedrooms = db.Column(db.Integer)

    bathrooms = db.Column(db.Integer)

    price = db.Column(
        db.Numeric(10, 2)
    )

    status = db.Column(db.String(50))

    image_url = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Many properties belong to one landlord
    landlord = db.relationship(
        "User",
        back_populates="properties"
    )

    # One property has many bookings
    bookings = db.relationship(
        "Booking",
        back_populates="property",
        lazy=True
    )

    # One property has many reviews
    reviews = db.relationship(
        "Review",
        back_populates="property",
        lazy=True
    )

    # One property has many favorites
    favorites = db.relationship(
        "Favorite",
        back_populates="property",
        lazy=True
    )

    # One property has many maintenance requests
    maintenance_requests = db.relationship(
        "MaintenanceRequest",
        back_populates="property",
        lazy=True
    )

    # One property has many images
    images = db.relationship(
        "PropertyImage",
        back_populates="property",
        lazy=True
    )

    # Many properties can have many amenities
    amenities = db.relationship(
        "Amenity",
        secondary=property_amenities,
        back_populates="properties"
    )


# =====================================================
# BOOKING
# =====================================================

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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

    check_in = db.Column(
        db.Date,
        nullable=False
    )

    check_out = db.Column(
        db.Date,
        nullable=False
    )

    total_amount = db.Column(
        db.Numeric(10, 2)
    )

    booking_status = db.Column(
        db.String(50)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Many bookings belong to one property
    property = db.relationship(
        "Property",
        back_populates="bookings"
    )

    # Many bookings belong to one tenant
    tenant = db.relationship(
        "User",
        back_populates="bookings"
    )

    # One booking has one payment
    payment = db.relationship(
        "Payment",
        back_populates="booking",
        uselist=False
    )


# =====================================================
# PAYMENT
# =====================================================

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    booking_id = db.Column(
        db.Integer,
        db.ForeignKey("bookings.id"),
        nullable=False,
        unique=True
    )

    amount = db.Column(
        db.Numeric(10, 2)
    )

    payment_method = db.Column(
        db.String(50)
    )

    payment_status = db.Column(
        db.String(50)
    )

    transaction_id = db.Column(
        db.String(100)
    )

    payment_date = db.Column(
        db.DateTime
    )

    # One payment belongs to one booking
    booking = db.relationship(
        "Booking",
        back_populates="payment"
    )


# =====================================================
# REVIEW
# =====================================================

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Many reviews belong to one property
    property = db.relationship(
        "Property",
        back_populates="reviews"
    )

    # Many reviews belong to one tenant
    tenant = db.relationship(
        "User",
        back_populates="reviews"
    )


# =====================================================
# FAVORITE
# =====================================================

class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Many favorites belong to one user
    user = db.relationship(
        "User",
        back_populates="favorites"
    )

    # Many favorites belong to one property
    property = db.relationship(
        "Property",
        back_populates="favorites"
    )


# =====================================================
# MAINTENANCE REQUEST
# =====================================================

class MaintenanceRequest(db.Model):
    __tablename__ = "maintenance_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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

    status = db.Column(
        db.String(50)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Many maintenance requests belong to one property
    property = db.relationship(
        "Property",
        back_populates="maintenance_requests"
    )

    # Many maintenance requests belong to one tenant
    tenant = db.relationship(
        "User",
        back_populates="maintenance_requests"
    )


# =====================================================
# PROPERTY IMAGE
# =====================================================

class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    image_url = db.Column(
        db.String(255)
    )

    # Many images belong to one property
    property = db.relationship(
        "Property",
        back_populates="images"
    )


# =====================================================
# AMENITY
# =====================================================

class Amenity(db.Model):
    __tablename__ = "amenities"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True
    )

    # Many amenities belong to many properties
    properties = db.relationship(
        "Property",
        secondary=property_amenities,
        back_populates="amenities"
    )