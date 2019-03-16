from marshmallow import Schema, fields, validate
from main.libs.validator import must_not_be_blank


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=must_not_be_blank)
    password = fields.Str(required=True, validate=validate.Length(min=6))
