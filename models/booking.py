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

    def to_dict(self):
        return {
            "id": self.id,
            "property_id": self.property_id,
            "property_title": self.property.title if self.property else None,
            "property_city": self.property.city if self.property else None,
            "tenant_id": self.tenant_id,
            "tenant_name": f"{self.tenant.first_name} {self.tenant.last_name}" if self.tenant else None,
            "check_in": self.check_in.isoformat() if self.check_in else None,
            "check_out": self.check_out.isoformat() if self.check_out else None,
            "total_amount": float(self.total_amount) if self.total_amount is not None else None,
            "booking_status": self.booking_status,
            "has_payment": self.payment is not None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }