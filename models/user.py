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

    reset_token = db.Column(db.String(200))
    reset_token_expires = db.Column(db.DateTime)

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

    def to_dict(self, private=False):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": f"{self.first_name} {self.last_name}",
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"name='{self.first_name} {self.last_name}', "
            f"role='{self.role}')>"
        )