from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from main import app
from main.models.category import CategoryModel
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
    try:
        CategoryModel.query.get(cat_id)
    except IntegrityError:
        return jsonify({'message': 'Category could not be found.'}), 404
    items = ItemModel.query.filter_by(cat_id=cat_id).all()
    result = items_schema.dump(items)
    return jsonify({'items': result.data}), 200


# Create an item to a category
@app.route('/categories/<int:cat_id>/items', methods=['POST'])
def create_item_to_category(cat_id):
    user_id = 1
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = item_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    try:
        CategoryModel.query.get(cat_id)
    except IntegrityError:
        return jsonify({'message': 'Category could not be found.'}), 404

    title, description = data[0]['title'], data[0]['description']
    item = ItemModel(title, description, cat_id, user_id)
    item.save_to_db()
    return jsonify({'message': 'Created item successfully.'}), 201


# Update existed item
@app.route('/categories/<int:cat_id>/items/<int:item_id>', methods=['PUT'])
def update_item_from_category(user_id, cat_id, item_id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = item_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    try:
        CategoryModel.query.get(cat_id)
    except IntegrityError:
        return jsonify({'message': 'Category could not be found.'}), 404

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
def delete_item_from_category(user_id, cat_id, item_id):
    try:
        CategoryModel.query.get(cat_id)
    except IntegrityError:
        return jsonify({'message': 'Category could not be found.'}), 404

    item = ItemModel.query.get(item_id)
    if item:
        if item.user_id != user_id:
            return jsonify({'message': 'Permission denied.'}), 550
    else:
        return jsonify({'message': 'Item could not be found'}), 404

    item.delete_from_db()
    return jsonify({'message': 'Deleted item successfully.'}), 200
