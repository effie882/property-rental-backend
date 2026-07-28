from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Property, User, Amenity
from utils import host_required

property_bp = Blueprint("properties", __name__)


@property_bp.route("/", methods=["GET"])
def get_properties():
    query = Property.query
    status = request.args.get("status")
    property_type = request.args.get("property_type")
    city = request.args.get("city")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    bedrooms = request.args.get("bedrooms", type=int)
    bathrooms = request.args.get("bathrooms", type=int)

    if status:
        query = query.filter(Property.status == status)
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    if max_price is not None:
        query = query.filter(Property.price <= max_price)
    if bedrooms is not None:
        query = query.filter(Property.bedrooms == bedrooms)
    if bathrooms is not None:
        query = query.filter(Property.bathrooms == bathrooms)

    properties = query.order_by(Property.created_at.desc()).all()
    return jsonify([p.to_dict() for p in properties]), 200


@property_bp.route("/<int:id>", methods=["GET"])
def get_property(id):
    prop = db.session.get(Property, id)
    if prop is None:
        return jsonify({"error": "Property not found"}), 404
    return jsonify(prop.to_dict()), 200


@property_bp.route("/", methods=["POST"])
@jwt_required()
@host_required
def create_property():
    user_id = get_jwt_identity()
    data = request.get_json()
    required = ["title", "price"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    prop = Property(
        landlord_id=user_id,
        title=data["title"].strip(),
        description=data.get("description"),
        address=data.get("address"),
        city=data.get("city"),
        county=data.get("county"),
        property_type=data.get("property_type"),
        bedrooms=data.get("bedrooms"),
        bathrooms=data.get("bathrooms"),
        price=data["price"],
        status=data.get("status", "available"),
        image_url=data.get("image_url"),
    )

    amenity_ids = data.get("amenity_ids", [])
    if amenity_ids:
        amenities = Amenity.query.filter(Amenity.id.in_(amenity_ids)).all()
        prop.amenities = amenities

    db.session.add(prop)
    db.session.commit()
    return jsonify({"message": "Property created", "property": prop.to_dict()}), 201


@property_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@host_required
def update_property(id):
    prop = db.session.get(Property, id)
    if prop is None:
        return jsonify({"error": "Property not found"}), 404

    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if prop.landlord_id != user_id and user.role != "admin":
        return jsonify({"error": "You do not own this property"}), 403

    data = request.get_json()
    fields = [
        "title", "description", "address", "city", "county",
        "property_type", "bedrooms", "bathrooms", "price",
        "status", "image_url"
    ]
    for field in fields:
        if field in data:
            setattr(prop, field, data[field])

    if "amenity_ids" in data:
        amenity_ids = data["amenity_ids"]
        amenities = Amenity.query.filter(Amenity.id.in_(amenity_ids)).all()
        prop.amenities = amenities

    db.session.commit()
    return jsonify({"message": "Property updated", "property": prop.to_dict()}), 200


@property_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@host_required
def delete_property(id):
    prop = db.session.get(Property, id)
    if prop is None:
        return jsonify({"error": "Property not found"}), 404

    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if prop.landlord_id != user_id and user.role != "admin":
        return jsonify({"error": "You do not own this property"}), 403

    db.session.delete(prop)
    db.session.commit()
    return jsonify({"message": "Property deleted"}), 200


@property_bp.route("/host/mine", methods=["GET"])
@jwt_required()
@host_required
def get_my_properties():
    user_id = get_jwt_identity()
    properties = Property.query.filter_by(landlord_id=user_id).order_by(Property.created_at.desc()).all()
    return jsonify([p.to_dict() for p in properties]), 200