from marshmallow import ValidationError


# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')
