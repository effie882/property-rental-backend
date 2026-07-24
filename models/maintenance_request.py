from datetime import datetime

from . import db


class MaintenanceRequest(db.Model):
    __tablename__ = "maintenance_requests"

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

    issue = db.Column(
        db.Text
    )

    status = db.Column(
        db.String(50)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Many maintenance requests belong to one property
    property = db.relationship(
        "Property",
        back_populates="maintenance_requests"
    )

    # Many maintenance requests belong to one tenant
    tenant = db.relationship(
        "User",
        back_populates="maintenance_requests"
    )