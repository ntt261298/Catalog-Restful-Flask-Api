from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from main import app
from main.models.user import UserModel
from main.schemas.user import UserSchema
from main.models.item import ItemModel
from main.schemas.item import ItemSchema
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

user_schema = UserSchema()
items_schema = ItemSchema(many=True)


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
    # Create access token
    access_token = create_access_token(identity=data[0]['username'])
    refresh_token = create_refresh_token(identity=data[0]['username'])
    return jsonify({'message': 'Created user successfully.',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }), 201


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
        access_token = create_access_token(identity=data[0]['username'])
        refresh_token = create_refresh_token(identity=data[0]['username'])
        return jsonify({'message': 'Logged in as {}.'.format(user.username),
                        'access_token': access_token,
                        'refresh_token': refresh_token
                        }), 200
    return jsonify({'message': 'Wrong credentials.'}), 404


# Get all user's items
@app.route('/users/items', methods=['GET'])
@jwt_required
def user_items():
    # Get user from JWT token
    current_user = get_jwt_identity()
    user_id = UserModel.query.filter_by(username=current_user).first().id

    items = ItemModel.query.filter_by(user_id=user_id).all()
    result = items_schema.dump(items)
    return jsonify({'items': result.data}), 200
