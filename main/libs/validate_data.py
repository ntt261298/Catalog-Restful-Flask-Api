from functools import wraps

from flask import request, jsonify
from marshmallow import ValidationError


def validate_data(schema):
    def my_decorator(func):
        @wraps(func)
        def my_func(*args, **kwargs):
            json_data = request.get_json()
            if not json_data:
                return jsonify({'message': 'No input data provided.'}), 400
            # Validate and deserialize input
            try:
                data = schema.load(json_data).data
            except ValidationError as err:
                return jsonify(err.messages), 400

            return func(data, *args, **kwargs)
        return my_func
    return my_decorator
