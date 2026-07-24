from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.review   import Review
from app.models.property import Property
from app.models.user     import User

reviews_bp = Blueprint("reviews", __name__)


# GET /api/reviews/property/<property_id>
@reviews_bp.route("/property/<int:property_id>", methods=["GET"])
def get_property_reviews(property_id):
    Property.query.get_or_404(property_id)
    reviews = Review.query.filter_by(
        property_id=property_id
    ).order_by(Review.created_at.desc()).all()
    return jsonify([r.to_dict() for r in reviews]), 200


# GET /api/reviews/<id> 
@reviews_bp.route("/<int:id>", methods=["GET"])
def get_review(id):
    review = Review.query.get_or_404(id)
    return jsonify(review.to_dict()), 200


# POST /api/reviews
@reviews_bp.route("/", methods=["POST"])
@jwt_required()
def create_review():
    user_id = get_jwt_identity()
    data    = request.get_json()

    required = ["property_id", "rating"]
    missing  = [f for f in required if data.get(f) is None]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if not (1 <= int(data["rating"]) <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    prop = Property.query.get_or_404(data["property_id"])

    if prop.host_id == user_id:
        return jsonify({"error": "Hosts cannot review their own property"}), 403

    existing = Review.query.filter_by(
        guest_id=user_id, property_id=data["property_id"]
    ).first()
    if existing:
        return jsonify({"error": "You have already reviewed this property"}), 409

    review = Review(
        rating      = int(data["rating"]),
        comment     = data.get("comment"),
        guest_id    = user_id,
        property_id = data["property_id"],
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review posted", "review": review.to_dict()}), 201


#  PUT /api/reviews/<id>
@reviews_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_review(id):
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)
    review  = Review.query.get_or_404(id)

    if review.guest_id != user_id and user.role != "admin":
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


# DELETE /api/reviews/<id> 
@reviews_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_review(id):
    user_id = get_jwt_identity()
    user    = User.query.get(user_id)
    review  = Review.query.get_or_404(id)

    if review.guest_id != user_id and user.role != "admin":
        return jsonify({"error": "You can only delete your own reviews"}), 403

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"}), 200