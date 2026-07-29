from marshmallow import fields, validate
from models import ma, Property
from schemas.amenity import AmenitySchema


class PropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Property
        load_instance = False
        include_fk = True

    id            = ma.auto_field(dump_only=True)
    landlord_id   = ma.auto_field(dump_only=True)
    landlord_name = fields.Method("get_landlord_name", dump_only=True)
    title         = fields.String(required=True, validate=validate.Length(min=1, max=150))
    description   = fields.String(allow_none=True)
    address       = fields.String(allow_none=True, validate=validate.Length(max=255))
    city          = fields.String(allow_none=True, validate=validate.Length(max=100))
    county        = fields.String(allow_none=True, validate=validate.Length(max=100))
    property_type = fields.String(allow_none=True, validate=validate.OneOf(
        ["apartment", "house", "villa", "studio", "cottage", "bungalow", "lodge"]))
    bedrooms      = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    bathrooms     = fields.Integer(allow_none=True, validate=validate.Range(min=0))
    price         = fields.Decimal(required=True, places=2, validate=validate.Range(min=0), as_string=False)
    status        = fields.String(validate=validate.OneOf(
        ["available", "booked", "maintenance", "unavailable"]))
    image_url     = fields.String(allow_none=True, validate=validate.Length(max=255))
    avg_rating    = fields.Method("get_avg_rating", dump_only=True)
    review_count  = fields.Method("get_review_count", dump_only=True)
    amenities     = fields.Nested(AmenitySchema, many=True, dump_only=True)
    amenity_ids   = fields.List(fields.Integer(), load_only=True, required=False)
    created_at    = fields.DateTime(dump_only=True)

    def get_landlord_name(self, obj):
        return f"{obj.landlord.first_name} {obj.landlord.last_name}" if obj.landlord else None

    def get_avg_rating(self, obj):
        if not obj.reviews:
            return None
        return round(sum(r.rating for r in obj.reviews) / len(obj.reviews), 1)

    def get_review_count(self, obj):
        return len(obj.reviews)


property_schema   = PropertySchema()
properties_schema = PropertySchema(many=True)