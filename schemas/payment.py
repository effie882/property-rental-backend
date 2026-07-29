from marshmallow import fields, validate
from models import ma, Payment


class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        load_instance = False
        include_fk = True

    id              = ma.auto_field(dump_only=True)
    booking_id      = fields.Integer(required=True)
    amount          = fields.Decimal(required=True, places=2, validate=validate.Range(min=0), as_string=False)
    payment_method  = fields.String(required=True, validate=validate.OneOf(
        ["mpesa", "card", "bank_transfer"]))
    payment_status  = fields.String(validate=validate.OneOf(
        ["pending", "completed", "failed", "refunded"]))
    transaction_id  = fields.String(allow_none=True, validate=validate.Length(max=100))
    payment_date    = fields.DateTime(dump_only=True)


payment_schema  = PaymentSchema()
payments_schema = PaymentSchema(many=True)