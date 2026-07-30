from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User
from utils import admin_required

user_bp = Blueprint("users", __name__)


@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user = db.session.get(User, get_jwt_identity())
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict(private=True)), 200


@user_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_me():
    user = db.session.get(User, get_jwt_identity())
    if user is None:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if "first_name" in data and data["first_name"].strip():
        user.first_name = data["first_name"].strip()
    if "last_name" in data and data["last_name"].strip():
        user.last_name = data["last_name"].strip()
    if "phone" in data:
        user.phone = data["phone"]
    if "email" in data:
        email = data["email"].lower().strip()
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user.id:
            return jsonify({"error": "Email already in use"}), 409
        user.email = email

    db.session.commit()
    return jsonify({"message": "Profile updated", "user": user.to_dict(private=True)}), 200


@user_bp.route("/me/upgrade-to-host", methods=["PUT"])
@jwt_required()
def upgrade_to_host():
    user = db.session.get(User, get_jwt_identity())
    if user is None:
        return jsonify({"error": "User not found"}), 404
    if user.role == "landlord":
        return jsonify({"message": "Already a host", "user": user.to_dict(private=True)}), 200
    user.role = "landlord"
    db.session.commit()
    return jsonify({"message": "Account upgraded to host", "user": user.to_dict(private=True)}), 200


@user_bp.route("/me", methods=["DELETE"])
@jwt_required()
def delete_account():
    user = db.session.get(User, get_jwt_identity())
    if user is None:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 200


@user_bp.route("/", methods=["GET"])
@jwt_required()
@admin_required
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


@user_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
@admin_required
def get_user(id):
    user = db.session.get(User, id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200