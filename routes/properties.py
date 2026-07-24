from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.property import Property
from app.models.amenity  import Amenity
from app.models.user     import User
from app.utils.decorators import host_required

properties_bp = Blueprint("properties", __name__)


#  GET /api/properties
@properties_bp.route("/", methods=["GET"])
def get_properties():
    query = Property.query.filter_by(is_available=True)

    # Optional filters
    location  = request.args.get("location")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    smoking   = request.args.get("smoking")
    pets      = request.args.get("pet_friendly")
    access    = request.args.get("disability_access")
    guests    = request.args.get("guests", type=int)

    if location:
        query = query.filter(Property.location.ilike(f"%{location}%"))
    if min_price is not None:
        query = query.filter(Property.price_per_night >= min_price)
    if max_price is not None:
        query = query.filter(Property.price_per_night <= max_price)
    if smoking == "true":
        query = query.filter(Property.smoking_allowed == True)
    if pets == "true":
        query = query.filter(Property.pet_friendly == True)
    if access == "true":
        query = query.filter(Property.disability_access == True)
    if guests:
        query = query.filter(Property.max_guests >= guests)

    properties = query.order_by(Property.created_at.desc()).all()
    return jsonify([p.to_dict(include_amenities=True) for p in properties]), 200


# GET /api/properties/<id>
@properties_bp.route("/<int:id>", methods=["GET"])
def get_property(id):
    prop = Property.query.get_or_404(id)
    return jsonify(prop.to_dict(include_amenities=True)), 200


# POST /api/properties 
@properties_bp.route("/", methods=["POST"])
@jwt_required()
@host_required
def create_property():
    data = request.get_json()
    user_id = get_jwt_identity()

    required = ["title", "location", "price_per_night"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    prop = Property(
        title             = data["title"].strip(),
        description       = data.get("description"),
        location          = data["location"].strip(),
        price_per_night   = float(data["price_per_night"]),
        bedrooms          = data.get("bedrooms", 1),
        bathrooms         = data.get("bathrooms", 1),
        max_guests        = data.get("max_guests", 2),
        is_available      = data.get("is_available", True),
        smoking_allowed   = data.get("smoking_allowed", False),
        pet_friendly      = data.get("pet_friendly", False),
        disability_access = data.get("disability_access", False),
        host_id           = user_id,
    )

    # Attach amenities by id list
    amenity_ids = data.get("amenity_ids", [])
    if amenity_ids:
        amenities = Amenity.query.filter(Amenity.id.in_(amenity_ids)).all()
        prop.amenities = amenities

    db.session.add(prop)
    db.session.commit()
    return jsonify({"message": "Property created", "property": prop.to_dict(include_amenities=True)}), 201


#  PUT /api/properties/<id> 
@properties_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@host_required
def update_property(id):
    prop    = Property.query.get_or_404(id)
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)

    if prop.host_id != user_id and user.role != "admin":
        return jsonify({"error": "You do not own this property"}), 403

    data = request.get_json()
    fields = ["title", "description", "location", "price_per_night", "bedrooms",
              "bathrooms", "max_guests", "is_available", "smoking_allowed",
              "pet_friendly", "disability_access"]

    for field in fields:
        if field in data:
            setattr(prop, field, data[field])

    # Update amenities if provided
    if "amenity_ids" in data:
        amenities = Amenity.query.filter(Amenity.id.in_(data["amenity_ids"])).all()
        prop.amenities = amenities

    db.session.commit()
    return jsonify({"message": "Property updated", "property": prop.to_dict(include_amenities=True)}), 200


# DELETE /api/properties/<id>
@properties_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@host_required
def delete_property(id):
    prop    = Property.query.get_or_404(id)
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)

    if prop.host_id != user_id and user.role != "admin":
        return jsonify({"error": "You do not own this property"}), 403

    db.session.delete(prop)
    db.session.commit()
    return jsonify({"message": "Property deleted"}), 200


#GET /api/properties/host/mine 
@properties_bp.route("/host/mine", methods=["GET"])
@jwt_required()
@host_required
def get_my_properties():
    user_id    = get_jwt_identity()
    properties = Property.query.filter_by(host_id=user_id).order_by(Property.created_at.desc()).all()
    return jsonify([p.to_dict(include_amenities=True) for p in properties]), 200