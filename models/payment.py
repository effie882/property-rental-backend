from . import db


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

    def to_dict(self):
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "amount": float(self.amount) if self.amount is not None else None,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "transaction_id": self.transaction_id,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
        }