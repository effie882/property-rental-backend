from . import db


class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    image_url = db.Column(
        db.String(255)
    )

    # Many images belong to one property
    property = db.relationship(
        "Property",
        back_populates="images"
    )