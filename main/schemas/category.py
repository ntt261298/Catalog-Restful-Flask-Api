from marshmallow import Schema, fields

from main.libs.validator import must_not_be_blank


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=must_not_be_blank)
    items = fields.Nested('ItemSchema', many=True)

    class Meta:
        strict = True
