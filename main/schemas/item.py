from marshmallow import Schema, fields

from main.libs.validator import must_not_be_blank


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=must_not_be_blank)
    description = fields.Str(required=True, validate=must_not_be_blank)
    created_at = fields.DateTime(dump_only=True)
    category_id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)

    class Meta:
        strict = True
