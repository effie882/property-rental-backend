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

    def to_dict(self):
        return {
            "id": self.id,
            "property_id": self.property_id,
            "image_url": self.image_url,
        }