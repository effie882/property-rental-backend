from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Review, Property, User

review_bp = Blueprint("reviews", __name__)


@review_bp.route("/property/<int:property_id>", methods=["GET"])
def get_property_reviews(property_id):
    prop = db.session.get(Property, property_id)
    if prop is None:
        return jsonify({"error": "Property not found"}), 404
    reviews = Review.query.filter_by(property_id=property_id).order_by(Review.created_at.desc()).all()
    return jsonify([r.to_dict() for r in reviews]), 200


@review_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_review(id):
    review = db.session.get(Review, id)
    if review is None:
        return jsonify({"error": "Review not found"}), 404
    return jsonify(review.to_dict()), 200


@review_bp.route("/", methods=["POST"])
@jwt_required()
def create_review():
    user_id = get_jwt_identity()
    data = request.get_json()

    required = ["property_id", "rating"]
    missing = [f for f in required if data.get(f) is None]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if not (1 <= int(data["rating"]) <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    prop = db.session.get(Property, data["property_id"])
    if prop is None:
        return jsonify({"error": "Property not found"}), 404

    if prop.landlord_id == user_id:
        return jsonify({"error": "Hosts cannot review their own property"}), 403

    existing = Review.query.filter_by(
        tenant_id=user_id, property_id=data["property_id"]
    ).first()
    if existing:
        return jsonify({"error": "You have already reviewed this property"}), 409

    review = Review(
        rating=int(data["rating"]),
        comment=data.get("comment"),
        tenant_id=user_id,
        property_id=data["property_id"],
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review posted", "review": review.to_dict()}), 201


@review_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_review(id):
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    review = db.session.get(Review, id)
    if review is None:
        return jsonify({"error": "Review not found"}), 404

    if review.tenant_id != user_id and user.role != "admin":
        return jsonify({"error": "You can only edit your own reviews"}), 403

    data = request.get_json()
    if "rating" in data:
        if not (1 <= int(data["rating"]) <= 5):
            return jsonify({"error": "Rating must be between 1 and 5"}), 400
        review.rating = int(data["rating"])
    if "comment" in data:
        review.comment = data["comment"]

    db.session.commit()
    return jsonify({"message": "Review updated", "review": review.to_dict()}), 200


@review_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_review(id):
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    review = db.session.get(Review, id)
    if review is None:
        return jsonify({"error": "Review not found"}), 404

    if review.tenant_id != user_id and user.role != "admin":
        return jsonify({"error": "You can only delete your own reviews"}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"}), 200