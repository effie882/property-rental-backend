from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from models import Property, Amenity, User
from schemas.property import property_schema, properties_schema
from utils import landlord_required, validation_error_response


class PropertyListResource(Resource):
    """GET /api/properties  |  POST /api/properties"""

    def get(self):
        query = Property.query

        city          = request.args.get("city")
        county        = request.args.get("county")
        property_type = request.args.get("property_type")
        min_price     = request.args.get("min_price", type=float)
        max_price     = request.args.get("max_price", type=float)
        bedrooms      = request.args.get("bedrooms",  type=int)
        status        = request.args.get("status",    default="available")

        if city:          query = query.filter(Property.city.ilike(f"%{city}%"))
        if county:        query = query.filter(Property.county.ilike(f"%{county}%"))
        if property_type: query = query.filter(Property.property_type == property_type)
        if min_price:     query = query.filter(Property.price >= min_price)
        if max_price:     query = query.filter(Property.price <= max_price)
        if bedrooms:      query = query.filter(Property.bedrooms >= bedrooms)
        if status:        query = query.filter(Property.status == status)

        properties = query.order_by(Property.created_at.desc()).all()
        return properties_schema.dump(properties), 200

    @jwt_required()
    @landlord_required
    def post(self):
        user_id = get_jwt_identity()
        try:
            data = property_schema.load(request.get_json())
        except ValidationError as err:
            return validation_error_response(err)

        prop = Property(
            landlord_id   = user_id,
            title         = data["title"].strip(),
            description   = data.get("description"),
            address       = data.get("address"),
            city          = data.get("city"),
            county        = data.get("county"),
            property_type = data.get("property_type"),
            bedrooms      = data.get("bedrooms", 1),
            bathrooms     = data.get("bathrooms", 1),
            price         = data["price"],
            status        = data.get("status", "available"),
            image_url     = data.get("image_url"),
        )
        if data.get("amenity_ids"):
            prop.amenities = Amenity.query.filter(Amenity.id.in_(data["amenity_ids"])).all()

        db.session.add(prop)
        db.session.commit()
        return {"message": "Property created", "property": property_schema.dump(prop)}, 201


class PropertyResource(Resource):
    """GET /api/properties/<id>  |  PUT /api/properties/<id>  |  DELETE /api/properties/<id>"""

    def get(self, id):
        prop = Property.query.get_or_404(id)
        return property_schema.dump(prop), 200

    @jwt_required()
    @landlord_required
    def put(self, id):
        prop    = Property.query.get_or_404(id)
        user_id = get_jwt_identity()
        user    = User.query.get(user_id)
        if prop.landlord_id != user_id and user.role != "admin":
            return {"error": "You do not own this property"}, 403

        try:
            data = property_schema.load(request.get_json(), partial=True)
        except ValidationError as err:
            return validation_error_response(err)

        fields = ["title", "description", "address", "city", "county",
                  "property_type", "bedrooms", "bathrooms", "price", "status", "image_url"]
        for field in fields:
            if field in data:
                setattr(prop, field, data[field])
        if "amenity_ids" in data:
            prop.amenities = Amenity.query.filter(Amenity.id.in_(data["amenity_ids"])).all()

        db.session.commit()
        return {"message": "Property updated", "property": property_schema.dump(prop)}, 200

    @jwt_required()
    @landlord_required
    def delete(self, id):
        prop    = Property.query.get_or_404(id)
        user_id = get_jwt_identity()
        user    = User.query.get(user_id)
        if prop.landlord_id != user_id and user.role != "admin":
            return {"error": "You do not own this property"}, 403
        db.session.delete(prop)
        db.session.commit()
        return {"message": "Property deleted"}, 200


class LandlordPropertiesResource(Resource):
    """GET /api/properties/mine"""

    @jwt_required()
    @landlord_required
    def get(self):
        user_id = get_jwt_identity()
        user    = User.query.get(user_id)
        # NOTE: user.properties is a plain list (relationship has no lazy="dynamic")
        properties = sorted(user.properties, key=lambda p: p.created_at or 0, reverse=True)
        return properties_schema.dump(properties), 200