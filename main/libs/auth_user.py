from functools import wraps

from flask import request, jsonify
from flask_jwt_extended import decode_token

from main.models.user import Users
from main import app


def auth_user(func):
    @wraps(func)
    def my_func(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({'message': 'Unauthorized.'}), 401
        try:
            data = request.headers['Authorization'].encode('ascii', 'ignore')
            token = str.replace(str(data), 'Bearer ', '')

            username = decode_token(token)['identity']
        except Exception:
            return jsonify({'message': 'Invalid token.'}), 403

        try:
            current_user = Users.query.filter_by(username=username).one()
        except Exception:
            return jsonify({'message': 'Invalid user.'}), 404

        return func(current_user.id, *args, **kwargs)

    return my_func
