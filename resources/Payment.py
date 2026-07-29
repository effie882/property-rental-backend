from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Payment, Booking, User

payment_bp = Blueprint("payments", __name__)


@payment_bp.route("/", methods=["GET"])
@jwt_required()
def get_payments():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if user.role == "tenant":
        booking_ids = [b.id for b in user.bookings]
        payments = Payment.query.filter(Payment.booking_id.in_(booking_ids)).all()
    else:
        payments = Payment.query.all()

    return jsonify([p.to_dict() for p in payments]), 200


@payment_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_payment(id):
    payment = db.session.get(Payment, id)
    if payment is None:
        return jsonify({"error": "Payment not found"}), 404

    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    is_tenant = payment.booking.tenant_id == user_id
    is_host = payment.booking.property.landlord_id == user_id

    if not is_tenant and not is_host and user.role != "admin":
        return jsonify({"error": "Access denied"}), 403

    return jsonify(payment.to_dict()), 200


@payment_bp.route("/", methods=["POST"])
@jwt_required()
def create_payment():
    user_id = get_jwt_identity()
    data = request.get_json()

    required = ["booking_id", "amount", "payment_method"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    booking = db.session.get(Booking, data["booking_id"])
    if booking is None:
        return jsonify({"error": "Booking not found"}), 404

    if booking.tenant_id != user_id and not user.role == "admin":
        return jsonify({"error": "Access denied"}), 403

    payment = Payment(
        booking_id=data["booking_id"],
        amount=data["amount"],
        payment_method=data["payment_method"],
        payment_status=data.get("payment_status", "pending"),
        transaction_id=data.get("transaction_id"),
        payment_date=data.get("payment_date"),
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({"message": "Payment created", "payment": payment.to_dict()}), 201


@payment_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_payment(id):
    payment = db.session.get(Payment, id)
    if payment is None:
        return jsonify({"error": "Payment not found"}), 404

    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if payment.booking.tenant_id != user_id and user.role != "admin":
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    if "amount" in data:
        payment.amount = data["amount"]
    if "payment_method" in data:
        payment.payment_method = data["payment_method"]
    if "payment_status" in data:
        payment.payment_status = data["payment_status"]
    if "transaction_id" in data:
        payment.transaction_id = data["transaction_id"]
    if "payment_date" in data:
        payment.payment_date = data["payment_date"]

    db.session.commit()
    return jsonify({"message": "Payment updated", "payment": payment.to_dict()}), 200


@payment_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_payment(id):
    payment = db.session.get(Payment, id)
    if payment is None:
        return jsonify({"error": "Payment not found"}), 404

    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if payment.booking.tenant_id != user_id and user.role != "admin":
        return jsonify({"error": "Access denied"}), 403

    db.session.delete(payment)
    db.session.commit()
    return jsonify({"message": "Payment deleted"}), 200