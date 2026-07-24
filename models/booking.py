from datetime import datetime

from . import db


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