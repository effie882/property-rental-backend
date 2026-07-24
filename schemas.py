from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates_schema
)

# USER SCHEMA


class UserSchema(Schema):

    id = fields.Int(dump_only=True)

    first_name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    last_name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    email = fields.Email(
        required=True
    )

    password_hash = fields.Str(
        load_only=True,
        required=True
    )

    phone = fields.Str(
        validate=validate.Length(max=20)
    )

    role = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["landlord", "tenant", "admin"]
        )
    )

    created_at = fields.DateTime(
        dump_only=True
    )



# PROPERTY SCHEMA


class PropertySchema(Schema):

    id = fields.Int(
        dump_only=True
    )

    landlord_id = fields.Int(
        required=True
    )

    title = fields.Str(
        required=True,
        validate=validate.Length(
            min=1,
            max=150
        )
    )

    description = fields.Str()

    address = fields.Str()

    city = fields.Str()

    county = fields.Str()

    property_type = fields.Str()

    bedrooms = fields.Int(
        validate=validate.Range(min=0)
    )

    bathrooms = fields.Int(
        validate=validate.Range(min=0)
    )

    price = fields.Decimal(
        as_string=True,
        validate=validate.Range(min=0)
    )

    status = fields.Str(
        validate=validate.OneOf(
            [
                "available",
                "occupied",
                "maintenance"
            ]
        )
    )

    image_url = fields.Url(
        allow_none=True
    )

    created_at = fields.DateTime(
        dump_only=True
    )



# BOOKING SCHEMA


class BookingSchema(Schema):

    id = fields.Int(
        dump_only=True
    )

    property_id = fields.Int(
        required=True
    )

    tenant_id = fields.Int(
        required=True
    )

    check_in = fields.Date(
        required=True
    )

    check_out = fields.Date(
        required=True
    )

    total_amount = fields.Decimal(
        as_string=True,
        validate=validate.Range(min=0)
    )

    booking_status = fields.Str(
        validate=validate.OneOf(
            [
                "pending",
                "confirmed",
                "cancelled",
                "completed"
            ]
        )
    )

    created_at = fields.DateTime(
        dump_only=True
    )

    @validates_schema
    def validate_dates(
        self,
        data,
        **kwargs
    ):
        if data["check_out"] <= data["check_in"]:
            raise ValidationError(
                "Check-out date must be after check-in date.",
                "check_out"
            )


# PAYMENT SCHEMA


class PaymentSchema(Schema):

    id = fields.Int(
        dump_only=True
    )

    booking_id = fields.Int(
        required=True
    )

    amount = fields.Decimal(
        as_string=True,
        required=True,
        validate=validate.Range(min=0)
    )

    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf(
            [
                "mpesa",
                "card",
                "bank_transfer",
                "cash"
            ]
        )
    )

    payment_status = fields.Str(
        validate=validate.OneOf(
            [
                "pending",
                "completed",
                "failed",
                "refunded"
            ]
        )
    )

    transaction_id = fields.Str()

    payment_date = fields.DateTime(
        allow_none=True
    )



# REVIEW SCHEMA


class ReviewSchema(Schema):

    id = fields.Int(
        dump_only=True
    )

    property_id = fields.Int(
        required=True
    )

    tenant_id = fields.Int(
        required=True
    )

    rating = fields.Int(
        required=True,
        validate=validate.Range(
            min=1,
            max=5
        )
    )

    comment = fields.Str(
        validate=validate.Length(
            max=1000
        )
    )

    created_at = fields.DateTime(
        dump_only=True
    )



# FAVORITE SCHEMA


class FavoriteSchema(Schema):

    id = fields.Int(
        dump_only=True
    )

    user_id = fields.Int(
        required=True
    )

    property_id = fields.Int(
        required=True
    )

    created_at = fields.DateTime(
        dump_only=True
    )



# MAINTENANCE REQUEST SCHEMA


class MaintenanceRequestSchema(Schema):

    id = fields.Int(
        dump_only=True
    )

    property_id = fields.Int(
        required=True
    )

    tenant_id = fields.Int(
        required=True
    )

    issue = fields.Str(
        required=True,
        validate=validate.Length(
            min=1,
            max=1000
        )
    )

    status = fields.Str(
        validate=validate.OneOf(
            [
                "pending",
                "in_progress",
                "completed",
                "cancelled"
            ]
        )
    )

    created_at = fields.DateTime(
        dump_only=True
    )



# PROPERTY IMAGE SCHEMA

class PropertyImageSchema(Schema):

    id = fields.Int(
        dump_only=True
    )

    property_id = fields.Int(
        required=True
    )

    image_url = fields.Url(
        required=True
    )



# AMENITY SCHEMA


class AmenitySchema(Schema):

    id = fields.Int(
        dump_only=True
    )

    name = fields.Str(
        required=True,
        validate=validate.Length(
            min=1,
            max=100
        )
    )