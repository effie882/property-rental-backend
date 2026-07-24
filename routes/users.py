from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, bcrypt
from app.models.user import User

users_bp = Blueprint("users", __name__)


#GET /api/users/me 
@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user = User.query.get_or_404(get_jwt_identity())
    return jsonify(user.to_dict(private=True)), 200


# PUT /api/users/me 
@users_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_me():
    user = User.query.get_or_404(get_jwt_identity())
    data = request.get_json()

    if "name"  in data and data["name"].strip():
        user.name  = data["name"].strip()
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


# PUT /api/users/me/upgrade-to-host 
@users_bp.route("/me/upgrade-to-host", methods=["PUT"])
@jwt_required()
def upgrade_to_host():
    user = User.query.get_or_404(get_jwt_identity())
    if user.role == "host":
        return jsonify({"message": "Already a host", "user": user.to_dict(private=True)}), 200
    user.role = "host"
    db.session.commit()
    return jsonify({"message": "Account upgraded to host", "user": user.to_dict(private=True)}), 200


# PUT /api/users/me/preferences 
@users_bp.route("/me/preferences", methods=["PUT"])
@jwt_required()
def update_preferences():
    user = User.query.get_or_404(get_jwt_identity())
    data = request.get_json()

    if "pref_smoking"           in data:
        user.pref_smoking           = bool(data["pref_smoking"])
    if "pref_pet_friendly"      in data:
        user.pref_pet_friendly      = bool(data["pref_pet_friendly"])
    if "pref_disability_access" in data:
        user.pref_disability_access = bool(data["pref_disability_access"])

    db.session.commit()
    return jsonify({"message": "Preferences updated", "user": user.to_dict(private=True)}), 200


# DELETE /api/user
@users_bp.route("/me", methods=["DELETE"])
@jwt_required()
def delete_account():
    user = User.query.get_or_404(get_jwt_identity())
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted"}), 200