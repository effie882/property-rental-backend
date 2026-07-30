from marshmallow import fields, validate
from models import ma, MaintenanceRequest


class MaintenanceRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MaintenanceRequest
        load_instance = False
        include_fk = True

    id             = ma.auto_field(dump_only=True)
    property_id    = fields.Integer(required=True)
    tenant_id      = ma.auto_field(dump_only=True)
    property_title = fields.Method("get_property_title", dump_only=True)
    tenant_name    = fields.Method("get_tenant_name", dump_only=True)
    issue          = fields.String(required=True, validate=validate.Length(min=1, max=2000))
    status         = fields.String(validate=validate.OneOf(
        ["open", "in_progress", "resolved", "closed"]))
    created_at     = fields.DateTime(dump_only=True)

    def get_property_title(self, obj):
        return obj.property.title if obj.property else None

    def get_tenant_name(self, obj):
        return f"{obj.tenant.first_name} {obj.tenant.last_name}" if obj.tenant else None


maintenance_request_schema  = MaintenanceRequestSchema()
maintenance_requests_schema = MaintenanceRequestSchema(many=True)