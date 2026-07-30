from marshmallow import fields, validate
from models import ma, Review


class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = False
        include_fk = True

    id          = ma.auto_field(dump_only=True)
    property_id = fields.Integer(required=True)
    tenant_id   = ma.auto_field(dump_only=True)
    tenant_name = fields.Method("get_tenant_name", dump_only=True)
    rating      = fields.Integer(required=True, validate=validate.Range(min=1, max=5))
    comment     = fields.String(allow_none=True, validate=validate.Length(max=2000))
    created_at  = fields.DateTime(dump_only=True)

    def get_tenant_name(self, obj):
        return f"{obj.tenant.first_name} {obj.tenant.last_name}" if obj.tenant else None


review_schema  = ReviewSchema()
reviews_schema = ReviewSchema(many=True)