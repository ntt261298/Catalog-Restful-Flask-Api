from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from main import app
from main.models.user import UserModel
from main.schemas.user import UserSchema

user_schema = UserSchema()


# Register user
@app.route('/users', methods=['POST'])
def register_user():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    user = UserModel.query.filter_by(username=data[0]['username']).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400
    # Create new user with hash password
    new_user = UserModel(
        username=data[0]['username'],
        password=UserModel.generate_hash(data[0]['password'])
    )
    try:
        new_user.save_to_db()
    except IntegrityError:
        return jsonify({'message': 'Something went wrong.'}), 500
    return jsonify({'message': 'Created user successfully.'}), 201


# Authenticate user
@app.route('/users/auth', methods=['POST'])
def auth_user():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    user = UserModel.find_user_by_username(data[0]['username'])
    # Verify user
    if user and user.verify_hash(user.password, data[0]['password']):
        return jsonify({'message': 'Logged in as {}.'.format(user.username)}), 200
    return jsonify({'message': 'Wrong credentials.'}), 404
