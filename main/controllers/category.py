from flask import jsonify

from main import app
from main.models.category import Categories
from main.schemas.category import CategorySchema


@app.route('/categories', methods=['GET'])
def get_all_categories():
    """
    :return: All Categories
    """
    categories = Categories.query.all()
    # Serialize the queryset
    results = CategorySchema(many=True).dump(categories)
    return jsonify(results.data)
