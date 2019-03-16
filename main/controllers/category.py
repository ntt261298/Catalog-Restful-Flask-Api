from flask import jsonify, request
from flask_jwt import jwt_required
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from main import app
from main.models.category import CategoryModel
from main.schemas.category import CategorySchema

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@app.route('/categories', methods=['GET'])
def get_all_categories():
    categories = CategoryModel.query.all()
    # Serialize the queryset
    results = categories_schema.dump(categories)
    return jsonify({'categories': results}), 200


@app.route('/categories/<int:cat_id>', methods=['GET'])
def get_category(cat_id):
    try:
        category = CategoryModel.query.get(cat_id)
    except IntegrityError:
        return jsonify({'message': 'Category could not be found.'}), 404
    result = category_schema.dump(category)
    return jsonify({'item': result}), 200


@app.route('/categories', methods=['POST'])
def create_category():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = category_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    name = data['name']
    category = CategoryModel.query.get(name)

    if category:
        return jsonify({'message': 'Category already exists.'}), 400
    category = CategoryModel(name)
    category.save_to_db()
    return jsonify({'message': 'Created successfully.'}), 201


@app.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = category_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    try:
        category = CategoryModel.query.get(cat_id)
    except IntegrityError:
        return jsonify({'message': 'Category could not be found.'}), 404

    category.name = data['name']
    category.save_to_db()
    return jsonify({'message': 'Updated successfully.'}), 200


@app.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    try:
        category = CategoryModel.query.get(cat_id)
    except IntegrityError:
        return jsonify({'message': 'Category could not be found.'}), 404
    category.delete_from_db()
    return jsonify({'message': 'Deleted Successfully'}), 200
