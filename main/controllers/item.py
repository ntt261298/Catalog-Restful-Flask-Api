from flask import jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from main import app
from main.models.category import CategoryModel
from main.models.user import UserModel
from main.models.item import ItemModel
from main.schemas.item import ItemSchema

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    items = ItemModel.query.all()
    result = items_schema.dump(items)
    return jsonify({'items': result.data}), 200


# Get all items from a category
@app.route('/categories/<int:cat_id>/items', methods=['GET'])
def get_items_from_category(cat_id):
    if CategoryModel.query.get(cat_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404
    items = ItemModel.query.filter_by(cat_id=cat_id).all()
    result = items_schema.dump(items)
    return jsonify({'items': result.data}), 200


# Create an item to a category
@app.route('/categories/<int:cat_id>/items', methods=['POST'])
@jwt_required
def create_item_to_category(cat_id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = item_schema.load(json_data).data
    except ValidationError as err:
        return jsonify(err.messages), 422
    if CategoryModel.query.get(cat_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404

    # Get user from JWT token
    current_user = get_jwt_identity()
    user_id = UserModel.query.filter_by(username=current_user).first().id

    title, description = data['title'], data['description']
    item = ItemModel(title, description, cat_id, user_id)
    item.save_to_db()
    return jsonify({'message': 'Created item successfully.'}), 201


# Update existed item
@app.route('/categories/<int:cat_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required
def update_item_from_category(cat_id, item_id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = item_schema.load(json_data).data
    except ValidationError as err:
        return jsonify(err.messages), 422
    if CategoryModel.query.get(cat_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404

    # Get user from JWT token
    current_user = get_jwt_identity()
    user_id = UserModel.query.filter_by(username=current_user).first().id
    app.logger.info(user_id)

    item = ItemModel.query.get(item_id)
    if item:
        if item.user_id != user_id:
            return jsonify({'message': 'Permission denied.'}), 550
    else:
        return jsonify({'message': 'Item could not be found'}), 404

    item.title = data['title']
    item.description = data['description']
    item.save_to_db()
    return jsonify({'message': 'Updated item successfully.'}), 200


# Delete existed item
@app.route('/categories/<int:cat_id>/items/<int:item_id>', methods=['DELETE'])
@jwt_required
def delete_item_from_category(cat_id, item_id):
    if CategoryModel.query.get(cat_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404

    # Get user from JWT token
    current_user = get_jwt_identity()
    user_id = UserModel.query.filter_by(username=current_user).first().id
    app.logger.info(user_id)

    item = ItemModel.query.get(item_id)
    if item:
        if item.user_id != user_id:
            return jsonify({'message': 'Permission denied.'}), 550
    else:
        return jsonify({'message': 'Item could not be found'}), 404

    item.delete_from_db()
    return jsonify({'message': 'Deleted item successfully.'}), 200
