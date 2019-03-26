from flask import jsonify
from flask_jwt_extended import create_access_token

from main import app
from main.models.user import Users
from main.schemas.user import UserSchema
from main.libs.bcrypt_hash import generate_hash, verify_hash
from main.libs.database import db
from main.libs.validate_data import validate_data


@app.route('/users', methods=['POST'])
@validate_data(UserSchema())
def register_user(data):
    """
    :param data:
    :return: Register user and return access token, refresh token if success
    """
    user = Users.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({'message': 'User already exists.'}), 400

    # Create new user with hash password
    new_user = Users(
        username=data['username'],
        password=generate_hash(data['password'])
    )
    new_user.save_to_db()
    db.session.commit()
    # Create access token
    access_token = create_access_token(identity=data['username'])

    return jsonify({'message': 'Created user successfully.',
                    'access_token': access_token
                    }), 201


@app.route('/users/auth', methods=['POST'])
@validate_data(UserSchema())
def authenticate_user(data):
    """
    :param data:
    :return: Authenticate user successful or fail
    """
    user = Users.query.filter_by(username=data['username']).first()
    # Verify user
    if user and verify_hash(user.password, data['password']):
        access_token = create_access_token(identity=data['username'])
        return jsonify({'message': 'Logged in as {}.'.format(user.username),
                        'access_token': access_token
                        }), 200

    return jsonify({'message': 'Wrong credentials.'}), 404
