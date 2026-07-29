from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Booking, Property, User
from utils import host_required, calculate_total, has_booking_conflict

booking_bp = Blueprint("bookings", __name__)


@booking_bp.route("/", methods=["GET"])
@jwt_required()
def get_bookings():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if user.role in ("landlord", "admin"):
        property_ids = [p.id for p in user.properties]
        bookings = Booking.query.filter(
            Booking.property_id.in_(property_ids)
        ).order_by(Booking.check_in.desc()).all()
    else:
        bookings = Booking.query.filter_by(
            tenant_id=user_id
        ).order_by(Booking.check_in.desc()).all()

    return jsonify([b.to_dict() for b in bookings]), 200


@booking_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_booking(id):
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    booking = db.session.get(Booking, id)
    if booking is None:
        return jsonify({"error": "Booking not found"}), 404

    is_tenant = booking.tenant_id == user_id
    is_host = booking.property.landlord_id == user_id
    if not is_tenant and not is_host and user.role != "admin":
        return jsonify({"error": "Access denied"}), 403

    return jsonify(booking.to_dict()), 200


@booking_bp.route("/", methods=["POST"])
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    data = request.get_json()

    required = ["property_id", "check_in", "check_out"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    prop = db.session.get(Property, data["property_id"])
    if prop is None:
        return jsonify({"error": "Property not found"}), 404

    if prop.landlord_id == user_id:
        return jsonify({"error": "You cannot book your own property"}), 400

    try:
        total = calculate_total(prop.price, data["check_in"], data["check_out"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if has_booking_conflict(prop.id, data["check_in"], data["check_out"]):
        return jsonify({"error": "These dates are already booked for this property"}), 409

    booking = Booking(
        tenant_id=user_id,
        property_id=prop.id,
        check_in=data["check_in"],
        check_out=data["check_out"],
        total_amount=total,
        booking_status="confirmed",
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({"message": "Booking confirmed", "booking": booking.to_dict()}), 201


@booking_bp.route("/<int:id>/status", methods=["PUT"])
@jwt_required()
def update_booking_status(id):
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    booking = db.session.get(Booking, id)
    if booking is None:
        return jsonify({"error": "Booking not found"}), 404

    is_tenant = booking.tenant_id == user_id
    is_host = booking.property.landlord_id == user_id

    if not is_tenant and not is_host and user.role != "admin":
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    new_status = data.get("status")

    allowed_statuses = ["pending", "confirmed", "cancelled", "completed"]
    if new_status not in allowed_statuses:
        return jsonify({"error": f"Status must be one of: {', '.join(allowed_statuses)}"}), 400

    booking.booking_status = new_status
    db.session.commit()
    return jsonify({"message": f"Booking {new_status}", "booking": booking.to_dict()}), 200


@booking_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_booking(id):
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    booking = db.session.get(Booking, id)
    if booking is None:
        return jsonify({"error": "Booking not found"}), 404

    is_tenant = booking.tenant_id == user_id
    is_host = booking.property.landlord_id == user_id

    if not is_tenant and not is_host and user.role != "admin":
        return jsonify({"error": "Access denied"}), 403

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted"}), 200