from flask import jsonify

from main import app
from main.models.category import Categories
from main.models.item import Items
from main.schemas.item import ItemSchema
from main.libs.database import db
from main.libs.auth_user import auth_user
from main.libs.validate_data import validate_data


@app.route('/items', methods=['GET'])
def get_items():
    """
    :return: All items
    """
    items = Items.query.all()
    result = ItemSchema(many=True).dump(items)

    return jsonify(result.data)


@app.route('/categories/<int:category_id>/items', methods=['GET'])
def get_items_from_category(category_id):
    """
    :param category_id:
    :return: All items from a category which has id = category_id
    """
    if Categories.query.get(category_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404

    items = Items.query.filter_by(category_id=category_id).all()
    result = ItemSchema(many=True).dump(items)

    return jsonify(result.data)


@app.route('/categories/<int:category_id>/items/<int:item_id>',
           methods=['GET'])
def get_item_from_category(category_id, item_id):
    """
    :param category_id:
    :param item_id:
    :return: An item id=item_id from a category id=category_id
    """
    if Categories.query.get(category_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404
    if Items.query.get(item_id) is None:
        return jsonify({'message': 'Item could not be found.'}), 404

    item = Items.query.get(item_id)
    result = ItemSchema().dump(item)

    return jsonify(result.data)


@app.route('/categories/<int:category_id>/items', methods=['POST'])
@auth_user
@validate_data(ItemSchema())
def create_item(data, user_id, category_id):
    """
    :param data:
    :param user_id:
    :param category_id:
    :return: Created an item to a category successful or fail
    """
    if Categories.query.get(category_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404

    title, description = data['title'], data['description']
    item = Items(title, description, category_id, user_id)
    item.save_to_db()
    db.session.commit()

    return jsonify({'message': 'Created item successfully.'}), 201


@app.route('/categories/<int:category_id>/items/<int:item_id>',
           methods=['PUT'])
@auth_user
@validate_data(ItemSchema())
def update_item(data, user_id, category_id, item_id):
    """
    :param data:
    :param user_id:
    :param category_id:
    :param item_id:
    :return: Updated existed item successful or fail
    """
    if Categories.query.get(category_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404
    item = Items.query.get(item_id)
    if item is None:
        return jsonify({'message': 'Item could not be found.'}), 404
    if item.user_id != user_id:
        return jsonify({'message': 'Permission denied.'}), 550

    item.title = data['title']
    item.description = data['description']
    item.save_to_db()
    db.session.commit()

    return jsonify({'message': 'Updated item successfully.'})


@app.route('/categories/<int:category_id>/items/<int:item_id>',
           methods=['DELETE'])
@auth_user
def delete_item(user_id, category_id, item_id):
    """
    :param user_id:
    :param category_id:
    :param item_id:
    :return: Deleted item successful or fail
    """
    if Categories.query.get(category_id) is None:
        return jsonify({'message': 'Category could not be found.'}), 404
    item = Items.query.get(item_id)
    if item is None:
        return jsonify({'message': 'Item could not be found.'}), 404
    if item.user_id != user_id:
        return jsonify({'message': 'Permission denied.'}), 550

    item.delete_from_db()
    db.session.commit()

    return jsonify({'message': 'Deleted item successfully.'})
