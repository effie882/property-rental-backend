from datetime import datetime, date
from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from extensions import db
from models import User, Property, Booking


def host_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if user is None or user.role != "landlord":
            return jsonify({"error": "Host access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = db.session.get(User, user_id)
        if user is None or user.role != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


def calculate_total(price_per_night, check_in, check_out):
    if isinstance(check_in, str):
        check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
    if isinstance(check_out, str):
        check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
    if not isinstance(check_in, date):
        check_in = check_in.date()
    if not isinstance(check_out, date):
        check_out = check_out.date()
    nights = (check_out - check_in).days
    if nights <= 0:
        raise ValueError("Check-out date must be after check-in date")
    return float(price_per_night) * nights


def has_booking_conflict(property_id, check_in, check_out):
    if isinstance(check_in, str):
        check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
    if isinstance(check_out, str):
        check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
    if not isinstance(check_in, date):
        check_in = check_in.date()
    if not isinstance(check_out, date):
        check_out = check_out.date()
    conflicting = Booking.query.filter(
        Booking.property_id == property_id,
        Booking.check_in < check_out,
        Booking.check_out > check_in,
        Booking.booking_status != "cancelled"
    ).first()
    return conflicting is not None