from marshmallow import fields, validate, validates_schema, ValidationError
from models import ma, Booking


class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = False
        include_fk = True

    id              = ma.auto_field(dump_only=True)
    property_id     = fields.Integer(required=True)
    tenant_id       = ma.auto_field(dump_only=True)
    check_in        = fields.Date(required=True)
    check_out       = fields.Date(required=True)
    total_amount    = fields.Decimal(dump_only=True, places=2, as_string=False)
    booking_status  = fields.String(validate=validate.OneOf(
        ["pending", "confirmed", "cancelled", "completed"]))
    property_title  = fields.Method("get_property_title", dump_only=True)
    property_city   = fields.Method("get_property_city", dump_only=True)
    tenant_name     = fields.Method("get_tenant_name", dump_only=True)
    has_payment     = fields.Method("get_has_payment", dump_only=True)
    created_at      = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if "check_in" in data and "check_out" in data:
            if data["check_out"] <= data["check_in"]:
                raise ValidationError("check_out must be after check_in", field_name="check_out")

    def get_property_title(self, obj):
        return obj.property.title if obj.property else None

    def get_property_city(self, obj):
        return obj.property.city if obj.property else None

    def get_tenant_name(self, obj):
        return f"{obj.tenant.first_name} {obj.tenant.last_name}" if obj.tenant else None

    def get_has_payment(self, obj):
        return obj.payment is not None


class BookingStatusSchema(ma.Schema):
    booking_status = fields.String(required=True, validate=validate.OneOf(
        ["pending", "confirmed", "cancelled", "completed"]))


booking_schema       = BookingSchema()
bookings_schema      = BookingSchema(many=True)
booking_status_schema = BookingStatusSchema()