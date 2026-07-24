from . import db, property_amenities


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