from flask import jsonify

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





