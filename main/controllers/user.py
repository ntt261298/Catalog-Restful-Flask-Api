from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token

from main import app
from main.models.user import UserModel
from main.schemas.user import UserSchema
from main.libs.bcrypt_hash import generate_hash, verify_hash
from main.libs.database import db

user_schema = UserSchema()


@app.route('/users', methods=['POST'])
def register_user():
    """
    :return: Register user and return access token, refresh token if success
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = user_schema.load(json_data).data
        app.logger.info(user_schema.load(json_data).errors)
    except ValidationError as err:
        return jsonify(err.messages), 422

    user = UserModel.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400
    # Create new user with hash password
    new_user = UserModel(
        username=data['username'],
        password=generate_hash(data['password'])
    )
    try:
        new_user.save_to_db()
        db.session.commit()
    except IntegrityError:
        return jsonify({'message': 'Something went wrong.'}), 500
    # Create access token
    access_token = create_access_token(identity=data['username'])
    return jsonify({'message': 'Created user successfully.',
                    'access_token': access_token
                    }), 201


@app.route('/users/auth', methods=['POST'])
def authenticate_user():
    """
    :return: Authenticate user successful or fail
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = user_schema.load(json_data).data
    except ValidationError as err:
        return jsonify(err.messages), 422

    user = UserModel.find_user_by_username(data['username'])
    # Verify user
    if user and verify_hash(user.password, data['password']):
        access_token = create_access_token(identity=data['username'])
        return jsonify({'message': 'Logged in as {}.'.format(user.username),
                        'access_token': access_token
                        }), 200
    return jsonify({'message': 'Wrong credentials.'}), 404
