from flask import jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from main import app
from main.models.category import CategoryModel
from main.models.user import UserModel
from main.models.item import ItemModel
from main.schemas.item import ItemSchema
from main.libs.database import db

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


@app.route('/items', methods=['GET'])
def get_items():
    """
    :return: All items
    """
    items = ItemModel.query.all()
    result = items_schema.dump(items)
    return jsonify({'items': result.data}), 200


@app.route('/categories/<int:cat_id>/items', methods=['GET'])
def get_items_from_category(cat_id):
    """
    :param cat_id:
    :return: All items from a category which has id = cat_id
    """
    if CategoryModel.query.get(cat_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404
    items = ItemModel.query.filter_by(cat_id=cat_id).all()
    result = items_schema.dump(items)
    return jsonify({'items': result.data}), 200


@app.route('/categories/<int:cat_id>/items/<int:item_id>', methods=['GET'])
def get_item_from_category(cat_id, item_id):
    """
    :param cat_id:
    :param item_id:
    :return: An item id=item_id from a category id=cat_id
    """
    if CategoryModel.query.get(cat_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404
    if ItemModel.query.get(item_id) is None:
        return jsonify({'message': 'Item could not be found.'}), 404
    item = ItemModel.query.get(item_id)
    result = item_schema.dump(item)
    return jsonify({'item': result.data}), 200


@app.route('/categories/<int:cat_id>/items', methods=['POST'])
@jwt_required
def create_item_to_category(cat_id):
    """
    :param cat_id:
    :return: Created an item to a category successful or fail
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = item_schema.load(json_data).data
        app.logger.info(item_schema.load(json_data))
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
    db.session.commit()
    return jsonify({'message': 'Created item successfully.'}), 201


@app.route('/categories/<int:cat_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required
def update_item_from_category(cat_id, item_id):
    """
    :param cat_id:
    :param item_id:
    :return: Updated existed item successful or fail
    """
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
    if item is None:
        return jsonify({'message': 'Item could not be found.'}), 404
    if item.user_id != user_id:
        return jsonify({'message': 'Permission denied.'}), 550

    item.title = data['title']
    item.description = data['description']
    item.save_to_db()
    db.session.commit()
    return jsonify({'message': 'Updated item successfully.'}), 200


@app.route('/categories/<int:cat_id>/items/<int:item_id>', methods=['DELETE'])
@jwt_required
def delete_item_from_category(cat_id, item_id):
    """
    :param cat_id:
    :param item_id:
    :return: Deleted item successful or fail
    """
    if CategoryModel.query.get(cat_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404

    # Get user from JWT token
    current_user = get_jwt_identity()
    user_id = UserModel.query.filter_by(username=current_user).first().id
    app.logger.info(user_id)

    item = ItemModel.query.get(item_id)
    if item is None:
        return jsonify({'message': 'Item could not be found.'}), 404
    if item.user_id != user_id:
        return jsonify({'message': 'Permission denied.'}), 550

    item.delete_from_db()
    db.session.commit()
    return jsonify({'message': 'Deleted item successfully.'}), 200
