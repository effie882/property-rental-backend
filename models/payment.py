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