from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app import db
from models import Amenity
from schemas.amenity import amenity_schema, amenities_schema
from utils import admin_required, landlord_required, validation_error_response


class AmenityListResource(Resource):
    """GET /api/amenities  |  POST /api/amenities"""

    def get(self):
        amenities = Amenity.query.order_by(Amenity.name).all()
        return amenities_schema.dump(amenities), 200

    @jwt_required()
    @landlord_required
    def post(self):
        try:
            data = amenity_schema.load(request.get_json())
        except ValidationError as err:
            return validation_error_response(err)

        if Amenity.query.filter_by(name=data["name"].strip()).first():
            return {"error": "Amenity already exists"}, 409

        amenity = Amenity(name=data["name"].strip())
        db.session.add(amenity)
        db.session.commit()
        return {"message": "Amenity created", "amenity": amenity_schema.dump(amenity)}, 201


class AmenityResource(Resource):
    """GET /api/amenities/<id>  |  PUT /api/amenities/<id>  |  DELETE /api/amenities/<id>"""

    def get(self, id):
        return amenity_schema.dump(Amenity.query.get_or_404(id)), 200

    @jwt_required()
    @admin_required
    def put(self, id):
        amenity = Amenity.query.get_or_404(id)
        try:
            data = amenity_schema.load(request.get_json(), partial=True)
        except ValidationError as err:
            return validation_error_response(err)

        if "name" in data:
            amenity.name = data["name"].strip()
        db.session.commit()
        return {"message": "Amenity updated", "amenity": amenity_schema.dump(amenity)}, 200

    @jwt_required()
    @admin_required
    def delete(self, id):
        amenity = Amenity.query.get_or_404(id)
        db.session.delete(amenity)
        db.session.commit()
        return {"message": "Amenity deleted"}, 200
