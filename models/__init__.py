from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}



metadata = MetaData(
    naming_convention=naming_convention
)



db = SQLAlchemy(
    metadata=metadata
)

property_amenities = db.Table(
    "property_amenities",

    db.Column(
        "property_id",
        db.Integer,
        db.ForeignKey("properties.id"),
        primary_key=True
    ),

    db.Column(
        "amenity_id",
        db.Integer,
        db.ForeignKey("amenities.id"),
        primary_key=True
    )
)


# =====================================================
# IMPORT ALL MODELS
# =====================================================

from .amenity import Amenity as Amenity
from .booking import Booking as Booking
from .favorite import Favorite as Favorite
from .maintenance_request import MaintenanceRequest as MaintenanceRequest
from .payment import Payment as Payment
from .property import Property as Property
from .property_image import PropertyImage as PropertyImage
from .review import Review as Review
from .user import User as User

__all__ = [
    "Amenity",
    "Booking",
    "Favorite",
    "MaintenanceRequest",
    "Payment",
    "Property",
    "PropertyImage",
    "Review",
    "User",
]