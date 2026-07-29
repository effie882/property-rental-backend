from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from extensions import db
from models import Amenity
from schemas.amenity import amenity_schema, amenities_schema
from utils import admin_required, landlord_required, validation_error_response


amenities_bp = Blueprint("amenities", __name__)


@amenities_bp.route("/", methods=["GET"], strict_slashes=False)
def get_amenities():
    amenities = Amenity.query.order_by(Amenity.name).all()
    return jsonify(amenities_schema.dump(amenities)), 200


@amenities_bp.route("/", methods=["POST"])
@jwt_required()
@landlord_required
def create_amenity():
    try:
        data = amenity_schema.load(request.get_json())
    except Exception as err:
        return validation_error_response(err)

    if Amenity.query.filter_by(name=data["name"].strip()).first():
        return jsonify({"error": "Amenity already exists"}), 409

    amenity = Amenity(name=data["name"].strip())
    db.session.add(amenity)
    db.session.commit()
    return jsonify({"message": "Amenity created", "amenity": amenity_schema.dump(amenity)}), 201


@amenities_bp.route("/<int:id>", methods=["GET"])
def get_amenity(id):
    amenity = db.session.get(Amenity, id)
    if amenity is None:
        return jsonify({"error": "Amenity not found"}), 404
    return amenity_schema.dump(amenity), 200


@amenities_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_amenity(id):
    amenity = db.session.get(Amenity, id)
    if amenity is None:
        return jsonify({"error": "Amenity not found"}), 404

    try:
        data = amenity_schema.load(request.get_json(), partial=True)
    except Exception as err:
        return validation_error_response(err)

    if "name" in data:
        amenity.name = data["name"].strip()
    db.session.commit()
    return jsonify({"message": "Amenity updated", "amenity": amenity_schema.dump(amenity)}), 200


@amenities_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_amenity(id):
    amenity = db.session.get(Amenity, id)
    if amenity is None:
        return jsonify({"error": "Amenity not found"}), 404

    db.session.delete(amenity)
    db.session.commit()
    return jsonify({"message": "Amenity deleted"}), 200