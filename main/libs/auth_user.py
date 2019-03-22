from functools import wraps

from flask import request, jsonify
from flask_jwt_extended import decode_token

from main.models.user import UserModel
from main import app


def auth_user(func):
    @wraps(func)
    def my_func(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({'message': 'Unauthorized.'}), 401

        data = request.headers['Authorization'].encode('ascii', 'ignore')
        token = str.replace(str(data), 'Bearer ', '')
        try:
            username = decode_token(token)['identity']
        except Exception:
            return jsonify({'message': 'Invalid token.'}), 401

        current_user = UserModel.query.filter_by(username=username).first()

        if current_user is None:
            return jsonify({'message': 'Invalid user.'}), 404

        return func(current_user.id, *args, **kwargs)

    return my_func
