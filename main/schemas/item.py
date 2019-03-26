from marshmallow import Schema, fields, validate


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(dump_only=True)
    category_id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)

    class Meta:
        strict = True
