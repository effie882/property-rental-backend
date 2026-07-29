from datetime import datetime
from . import db, property_amenities


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
    description = db.Column(
        db.Text
    )
    address = db.Column(
        db.String(255)
    )
    city = db.Column(
        db.String(100)
    )
    county = db.Column(
        db.String(100)
    )
    property_type = db.Column(
        db.String(50)
    )
    bedrooms = db.Column(
        db.Integer
    )
    bathrooms = db.Column(
        db.Integer
    )
    price = db.Column(
        db.Numeric(10, 2)
    )
    status = db.Column(
        db.String(50)
    )
    image_url = db.Column(
        db.String(255)
    )
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
        back_populates="property"
    )
    # One property has many reviews
    reviews = db.relationship(
        "Review",
        back_populates="property"
    )
    # One property can have many favorites
    favorites = db.relationship(
        "Favorite",
        back_populates="property"
    )
    # One property can have many maintenance requests
    maintenance_requests = db.relationship(
        "MaintenanceRequest",
        back_populates="property"
    )
    # One property can have many images
    images = db.relationship(
        "PropertyImage",
        back_populates="property"
    )
    # Many properties can have many amenities
    amenities = db.relationship(
        "Amenity",
        secondary=property_amenities,
        back_populates="properties"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "landlord_id": self.landlord_id,
            "landlord_name": f"{self.landlord.first_name} {self.landlord.last_name}" if self.landlord else None,
            "title": self.title,
            "description": self.description,
            "address": self.address,
            "city": self.city,
            "county": self.county,
            "property_type": self.property_type,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "price": float(self.price) if self.price is not None else None,
            "status": self.status,
            "image_url": self.image_url,
            "amenities": [a.name for a in self.amenities] if self.amenities else [],
            "avg_rating": round(sum(r.rating for r in self.reviews) / len(self.reviews), 1) if self.reviews else None,
            "review_count": len(self.reviews) if self.reviews else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }