from marshmallow import fields
from models import ma, Favorite


class FavoriteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Favorite
        load_instance = False
        include_fk = True

    id             = ma.auto_field(dump_only=True)
    user_id        = ma.auto_field(dump_only=True)
    property_id    = fields.Integer(required=True)
    property_title = fields.Method("get_property_title", dump_only=True)
    property_city  = fields.Method("get_property_city", dump_only=True)
    property_price = fields.Method("get_property_price", dump_only=True)
    image_url      = fields.Method("get_image_url", dump_only=True)
    created_at     = fields.DateTime(dump_only=True)

    def get_property_title(self, obj):
        return obj.property.title if obj.property else None

    def get_property_city(self, obj):
        return obj.property.city if obj.property else None

    def get_property_price(self, obj):
        return float(obj.property.price) if obj.property and obj.property.price is not None else None

    def get_image_url(self, obj):
        return obj.property.image_url if obj.property else None


favorite_schema  = FavoriteSchema()
favorites_schema = FavoriteSchema(many=True)