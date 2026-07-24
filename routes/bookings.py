from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.booking  import Booking
from app.models.property import Property
from app.models.user     import User
from app.utils.helpers   import calculate_total, has_booking_conflict

bookings_bp = Blueprint("bookings", __name__)


# GET /api/bookings 
@bookings_bp.route("/", methods=["GET"])
@jwt_required()
def get_bookings():
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)

    # Hosts see bookings on their properties; guests see their own bookings
    if user.role in ("host", "admin"):
        property_ids = [p.id for p in user.properties.all()]
        bookings = Booking.query.filter(
            Booking.property_id.in_(property_ids)
        ).order_by(Booking.check_in_date.desc()).all()
    else:
        bookings = Booking.query.filter_by(
            guest_id=user_id
        ).order_by(Booking.check_in_date.desc()).all()

    return jsonify([b.to_dict() for b in bookings]), 200


#  GET /api/bookings/<id>
@bookings_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_booking(id):
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)
    booking = Booking.query.get_or_404(id)

    # Only the guest or the host of the property can view the booking
    is_guest = booking.guest_id == user_id
    is_host  = booking.property.host_id == user_id
    if not is_guest and not is_host and user.role != "admin":
        return jsonify({"error": "Access denied"}), 403

    return jsonify(booking.to_dict()), 200


# POST /api/booking
@bookings_bp.route("/", methods=["POST"])
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    data    = request.get_json()

    required = ["property_id", "check_in_date", "check_out_date", "num_guests"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    prop = Property.query.get_or_404(data["property_id"])

    if not prop.is_available:
        return jsonify({"error": "This property is not available for booking"}), 400

    if prop.host_id == user_id:
        return jsonify({"error": "You cannot book your own property"}), 400

    if int(data["num_guests"]) > prop.max_guests:
        return jsonify({"error": f"Maximum guests allowed is {prop.max_guests}"}), 400

    try:
        total = calculate_total(prop.price_per_night, data["check_in_date"], data["check_out_date"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if has_booking_conflict(prop.id, data["check_in_date"], data["check_out_date"]):
        return jsonify({"error": "These dates are already booked for this property"}), 409

    booking = Booking(
        check_in_date  = data["check_in_date"],
        check_out_date = data["check_out_date"],
        total_price    = total,
        num_guests     = int(data["num_guests"]),
        status         = "confirmed",
        guest_id       = user_id,
        property_id    = prop.id,
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({"message": "Booking confirmed", "booking": booking.to_dict()}), 201


#  PUT /api/bookings/<id>/status 
@bookings_bp.route("/<int:id>/status", methods=["PUT"])
@jwt_required()
def update_booking_status(id):
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)
    booking = Booking.query.get_or_404(id)

    is_guest = booking.guest_id == user_id
    is_host  = booking.property.host_id == user_id

    if not is_guest and not is_host and user.role != "admin":
        return jsonify({"error": "Access denied"}), 403

    data       = request.get_json()
    new_status = data.get("status")

    allowed_statuses = ["pending", "confirmed", "cancelled", "completed"]
    if new_status not in allowed_statuses:
        return jsonify({"error": f"Status must be one of: {', '.join(allowed_statuses)}"}), 400

    # Guests can only cancel; hosts can confirm, complete or cancel
    if is_guest and new_status not in ("cancelled",):
        return jsonify({"error": "Guests can only cancel bookings"}), 403

    booking.status = new_status
    db.session.commit()
    return jsonify({"message": f"Booking {new_status}", "booking": booking.to_dict()}), 200


# DELETE /api/bookings/<id> 
@bookings_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_booking(id):
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)
    booking = Booking.query.get_or_404(id)

    is_guest = booking.guest_id == user_id
    is_host  = booking.property.host_id == user_id

    if not is_guest and not is_host and user.role != "admin":
        return jsonify({"error": "Access denied"}), 403

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"message": "Booking deleted"}), 200