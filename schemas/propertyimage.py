from marshmallow import fields, validate
from models import ma, PropertyImage


class PropertyImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PropertyImage
        load_instance = False
        include_fk = True

    id          = ma.auto_field(dump_only=True)
    property_id = ma.auto_field(dump_only=True)
    image_url   = fields.String(required=True, validate=validate.Length(min=1, max=255))


property_image_schema  = PropertyImageSchema()
property_images_schema = PropertyImageSchema(many=True)