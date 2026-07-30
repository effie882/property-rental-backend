from datetime import datetime

from . import db


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

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    comment = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    property = db.relationship(
        "Property",
        back_populates="reviews"
    )

    tenant = db.relationship(
        "User",
        back_populates="reviews"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "property_id": self.property_id,
            "tenant_id": self.tenant_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }