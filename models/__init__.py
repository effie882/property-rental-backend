from extensions import db

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