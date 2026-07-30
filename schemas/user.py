from marshmallow import fields, validate
from models import ma, User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = False
        exclude = ("password_hash", "reset_token", "reset_token_expires")

    id         = ma.auto_field(dump_only=True)
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    last_name  = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email      = fields.Email(required=True)
    phone      = fields.String(allow_none=True, validate=validate.Length(max=20))
    role       = fields.String(validate=validate.OneOf(["tenant", "landlord", "admin"]))
    full_name  = fields.Method("get_full_name", dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class RegisterSchema(ma.Schema):
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    last_name  = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email      = fields.Email(required=True)
    phone      = fields.String(allow_none=True, validate=validate.Length(max=20))
    password   = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
    role       = fields.String(validate=validate.OneOf(["tenant", "landlord"]), load_default="tenant")


class LoginSchema(ma.Schema):
    email    = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


user_schema     = UserSchema()
users_schema    = UserSchema(many=True)
register_schema = RegisterSchema()
login_schema    = LoginSchema()