from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.amenity  import Amenity
from app.utils.decorators import host_required, admin_required

amenities_bp = Blueprint("amenities", __name__)


# ── GET /api/amenities ────────────────────────────────────────────────────────
@amenities_bp.route("/", methods=["GET"])
def get_amenities():
    category  = request.args.get("category")
    query     = Amenity.query
    if category:
        query = query.filter_by(category=category)
    amenities = query.order_by(Amenity.category, Amenity.name).all()
    return jsonify([a.to_dict() for a in amenities]), 200


# ── GET /api/amenities/<id> ───────────────────────────────────────────────────
@amenities_bp.route("/<int:id>", methods=["GET"])
def get_amenity(id):
    amenity = Amenity.query.get_or_404(id)
    return jsonify(amenity.to_dict()), 200


# ── POST /api/amenities ───────────────────────────────────────────────────────
@amenities_bp.route("/", methods=["POST"])
@jwt_required()
@host_required
def create_amenity():
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"error": "Amenity name is required"}), 400

    if Amenity.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "An amenity with this name already exists"}), 409

    amenity = Amenity(
        name        = data["name"].strip(),
        category    = data.get("category", "customisation"),
        icon        = data.get("icon"),
        description = data.get("description"),
    )
    db.session.add(amenity)
    db.session.commit()
    return jsonify({"message": "Amenity created", "amenity": amenity.to_dict()}), 201


# ── PUT /api/amenities/<id> ───────────────────────────────────────────────────
@amenities_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_amenity(id):
    amenity = Amenity.query.get_or_404(id)
    data    = request.get_json()

    if "name"        in data: amenity.name        = data["name"].strip()
    if "category"    in data: amenity.category    = data["category"]
    if "icon"        in data: amenity.icon        = data["icon"]
    if "description" in data: amenity.description = data["description"]

    db.session.commit()
    return jsonify({"message": "Amenity updated", "amenity": amenity.to_dict()}), 200


# ── DELETE /api/amenities/<id> ────────────────────────────────────────────────
@amenities_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_amenity(id):
    amenity = Amenity.query.get_or_404(id)
    db.session.delete(amenity)
    db.session.commit()
    return jsonify({"message": "Amenity deleted"}), 200