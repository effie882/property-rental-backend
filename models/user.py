from datetime import datetime

from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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

    phone = db.Column(
        db.String(20)
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # One landlord can have many properties
    properties = db.relationship(
        "Property",
        back_populates="landlord"
    )

    # One tenant can have many bookings
    bookings = db.relationship(
        "Booking",
        back_populates="tenant"
    )

    # One tenant can write many reviews
    reviews = db.relationship(
        "Review",
        back_populates="tenant"
    )

    # One user can have many favorites
    favorites = db.relationship(
        "Favorite",
        back_populates="user"
    )

    # One tenant can have many maintenance requests
    maintenance_requests = db.relationship(
        "MaintenanceRequest",
        back_populates="tenant"
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"name='{self.first_name} {self.last_name}', "
            f"role='{self.role}')>"
        )