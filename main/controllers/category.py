from flask import jsonify
from flask_jwt import jwt_required
from sqlalchemy.exc import IntegrityError
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
        return jsonify({'message': 'Category could not be found'}), 400
    result = category_schema.dump(category)
    return jsonify({'item': result}), 200
