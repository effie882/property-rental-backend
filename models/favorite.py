from datetime import datetime

from . import db


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

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "property_id": self.property_id,
            "property_title": self.property.title if self.property else None,
            "property_city": self.property.city if self.property else None,
            "property_price": float(self.property.price) if self.property and self.property.price is not None else None,
            "image_url": self.property.image_url if self.property else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }