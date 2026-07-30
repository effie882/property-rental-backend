from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Favorite, Property, User

favourite_bp = Blueprint("favourites", __name__)


@favourite_bp.route("/", methods=["GET"])
@jwt_required()
def get_favourites():
    user_id = get_jwt_identity()
    favourites = Favorite.query.filter_by(user_id=user_id).order_by(Favorite.created_at.desc()).all()
    return jsonify([f.to_dict() for f in favourites]), 200


@favourite_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_favourite(id):
    favourite = db.session.get(Favorite, id)
    if favourite is None:
        return jsonify({"error": "Favourite not found"}), 404
    return jsonify(favourite.to_dict()), 200


@favourite_bp.route("/", methods=["POST"])
@jwt_required()
def create_favourite():
    user_id = get_jwt_identity()
    data = request.get_json()

    required = ["property_id"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if Favorite.query.filter_by(user_id=user_id, property_id=data["property_id"]).first():
        return jsonify({"error": "Property already in favourites"}), 409

    favourite = Favorite(
        user_id=user_id,
        property_id=data["property_id"],
    )
    db.session.add(favourite)
    db.session.commit()
    return jsonify({"message": "Property added to favourites", "favourite": favourite.to_dict()}), 201


@favourite_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_favourite(id):
    favourite = db.session.get(Favorite, id)
    if favourite is None:
        return jsonify({"error": "Favourite not found"}), 404

    user_id = get_jwt_identity()
    if favourite.user_id != user_id:
        return jsonify({"error": "Access denied"}), 403

    db.session.delete(favourite)
    db.session.commit()
    return jsonify({"message": "Favourite removed"}), 200