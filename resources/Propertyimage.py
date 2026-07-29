from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import PropertyImage, Property, User
from utils import host_required, admin_required

property_image_bp = Blueprint("property_images", __name__)


@property_image_bp.route("/", methods=["GET"])
def get_property_images():
    property_id = request.args.get("property_id", type=int)
    if property_id:
        images = PropertyImage.query.filter_by(property_id=property_id).all()
    else:
        images = PropertyImage.query.all()
    return jsonify([i.to_dict() for i in images]), 200


@property_image_bp.route("/<int:id>", methods=["GET"])
def get_property_image(id):
    image = db.session.get(PropertyImage, id)
    if image is None:
        return jsonify({"error": "Image not found"}), 404
    return jsonify(image.to_dict()), 200


@property_image_bp.route("/", methods=["POST"])
@jwt_required()
@host_required
def create_property_image():
    user_id = get_jwt_identity()
    data = request.get_json()

    required = ["property_id", "image_url"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    prop = db.session.get(Property, data["property_id"])
    if prop is None:
        return jsonify({"error": "Property not found"}), 404

    if prop.landlord_id != user_id:
        return jsonify({"error": "Access denied"}), 403

    image = PropertyImage(
        property_id=data["property_id"],
        image_url=data["image_url"],
    )
    db.session.add(image)
    db.session.commit()
    return jsonify({"message": "Image created", "image": image.to_dict()}), 201


@property_image_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@host_required
def update_property_image(id):
    image = db.session.get(PropertyImage, id)
    if image is None:
        return jsonify({"error": "Image not found"}), 404

    user_id = get_jwt_identity()
    if image.property.landlord_id != user_id:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    if "image_url" in data:
        image.image_url = data["image_url"]

    db.session.commit()
    return jsonify({"message": "Image updated", "image": image.to_dict()}), 200


@property_image_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@host_required
def delete_property_image(id):
    image = db.session.get(PropertyImage, id)
    if image is None:
        return jsonify({"error": "Image not found"}), 404

    user_id = get_jwt_identity()
    if image.property.landlord_id != user_id and get_jwt_identity() != user_id:
        return jsonify({"error": "Access denied"}), 403

    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "Image deleted"}), 200