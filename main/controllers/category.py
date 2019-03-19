from flask import jsonify, request
from marshmallow import ValidationError
from main import app
from main.models.category import CategoryModel
from main.schemas.category import CategorySchema

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


@app.route('/categories', methods=['GET'])
def get_all_categories():
    """
    :return: All Categories
    """
    categories = CategoryModel.query.all()
    # Serialize the queryset
    results = categories_schema.dump(categories)
    return jsonify({'categories': results.data}), 200


@app.route('/categories/<int:cat_id>', methods=['GET'])
def get_category(cat_id):
    """
    :param cat_id:
    :return: Category with id = cat_id
    """
    category = CategoryModel.query.get(cat_id)
    app.logger.info(category)

    if category is None:
        return jsonify({'message': 'Category could not be found.'}), 404
    result = category_schema.dump(category)
    return jsonify({'category': result.data}), 200


@app.route('/categories', methods=['POST'])
def create_category():
    """
    :return: Created new category successfully or fail
    """
    json_data = request.get_json()
    app.logger.info(json_data)
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = category_schema.load(json_data).data
    except ValidationError as err:
        return jsonify(err.messages), 422
    name = data['name']
    category = CategoryModel.query.filter_by(name=name).first()

    if category:
        return jsonify({'message': 'Category already exists.'}), 400

    category = CategoryModel(name)
    category.save_to_db()
    return jsonify({'message': 'Created category successfully.'}), 201


@app.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    """
    :param cat_id:
    :return: Updated existed category successfully or fail
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided.'}), 400
    # Validate and deserialize input
    try:
        data = category_schema.load(json_data).data
    except ValidationError as err:
        return jsonify(err.messages), 422

    category = CategoryModel.query.get(cat_id)
    if category is None:
        return jsonify({'message': 'Category could not be found.'}), 404

    category.name = data['name']
    category.save_to_db()
    return jsonify({'message': 'Updated category successfully.'}), 200


@app.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    """
    :param cat_id:
    :return: Deleted existed category successfully or fail
    """
    category = CategoryModel.query.get(cat_id)
    if category is None:
        return jsonify({'message': 'Category could not be found.'}), 404

    category.delete_from_db()
    return jsonify({'message': 'Deleted category Successfully'}), 200
