from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import MaintenanceRequest, Property, User
from utils import host_required, admin_required

maintenance_bp = Blueprint("maintenance", __name__)


@maintenance_bp.route("/", methods=["GET"])
@jwt_required()
def get_maintenance_requests():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    requests = MaintenanceRequest.query.all()
    if user.role == "tenant":
        requests = requests.filter(MaintenanceRequest.tenant_id == user_id)
    elif user.role == "landlord":
        property_ids = [p.id for p in user.properties]
        requests = requests.filter(MaintenanceRequest.property_id.in_(property_ids))

    requests = requests.order_by(MaintenanceRequest.created_at.desc()).all()
    return jsonify([r.to_dict() for r in requests]), 200


@maintenance_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_maintenance_request(id):
    req = db.session.get(MaintenanceRequest, id)
    if req is None:
        return jsonify({"error": "Maintenance request not found"}), 404
    return jsonify(req.to_dict()), 200


@maintenance_bp.route("/", methods=["POST"])
@jwt_required()
def create_maintenance_request():
    user_id = get_jwt_identity()
    data = request.get_json()

    required = ["property_id", "issue"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    prop = db.session.get(Property, data["property_id"])
    if prop is None:
        return jsonify({"error": "Property not found"}), 404

    maintenance_req = MaintenanceRequest(
        tenant_id=user_id,
        property_id=prop.id,
        issue=data["issue"],
        status=data.get("status", "pending"),
    )
    db.session.add(maintenance_req)
    db.session.commit()
    return jsonify({"message": "Maintenance request created", "maintenance_request": maintenance_req.to_dict()}), 201


@maintenance_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_maintenance_request(id):
    req = db.session.get(MaintenanceRequest, id)
    if req is None:
        return jsonify({"error": "Maintenance request not found"}), 404

    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    is_tenant = req.tenant_id == user_id
    is_host = req.property.landlord_id == user_id

    if not is_tenant and not is_host and user.role != "admin":
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    if "status" in data:
        req.status = data["status"]
    if "issue" in data:
        req.issue = data["issue"]

    db.session.commit()
    return jsonify({"message": "Maintenance request updated", "maintenance_request": req.to_dict()}), 200


@maintenance_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_maintenance_request(id):
    req = db.session.get(MaintenanceRequest, id)
    if req is None:
        return jsonify({"error": "Maintenance request not found"}), 404

    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    is_tenant = req.tenant_id == user_id
    is_host = req.property.landlord_id == user_id

    if not is_tenant and not is_host and user.role != "admin":
        return jsonify({"error": "Access denied"}), 403

    db.session.delete(req)
    db.session.commit()
    return jsonify({"message": "Maintenance request deleted"}), 200