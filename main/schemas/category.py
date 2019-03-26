from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    items = fields.Nested('ItemSchema', many=True)

    class Meta:
        strict = True
