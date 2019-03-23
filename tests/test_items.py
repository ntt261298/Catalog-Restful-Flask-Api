import unittest

import requests
from flask import json

from main import app, db
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel
from main.libs.bcrypt_hash import generate_hash
from config import app_config
import main.controllers


class CatalogApiTests(unittest.TestCase):
    username = 'truongnt'
    password = '123456'
    cat_name = 'Cat1'

    # Executed prior to each tests
    def setUp(self):
        with app.app_context():
            app.config.from_object(app_config['testing'])
            self.app = app.test_client()
            db.drop_all()
            db.create_all()
            self.create_users()
            self.create_categories()
            self.create_items()
            self.assertEqual(app.debug, False)

    # Executed after each tests
    def tearDown(self):
        with app.app_context():
            db.session.remove()

    # Helper methods
    def create_users(self):
        # Create a new user
        new_user = UserModel(self.username, generate_hash(self.password))
        new_user.save_to_db()
        test_user = UserModel('test', generate_hash('test123'))
        test_user.save_to_db()
        db.session.commit()
        return

    def create_categories(self):
        # Create a new category
        new_category = CategoryModel(self.cat_name)
        db.session.add(new_category)
        db.session.commit()
        return

    def create_items(self):
        user1 = UserModel.query.filter_by(username=self.username).first()
        cat1 = CategoryModel.query.filter_by(name=self.cat_name).first()

        item1 = ItemModel('Hamburgers',
                          'Classic dish elevated with pretzel buns.',
                          cat1.id,
                          user1.id)
        item2 = ItemModel('Mediterranean Chicken',
                          'Grilled chicken served with pitas and hummus',
                          cat1.id,
                          user1.id)
        item3 = ItemModel('Tacos', 'Ground beef tacos with grilled peppers.',
                          cat1.id,
                          user1.id)
        item4 = ItemModel('Homemade Pizza',
                          'Homemade pizza made using pizza oven',
                          cat1.id,
                          user1.id)
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.add(item4)
        db.session.commit()

    def authenticate_user(self, username, password):
        headers = {}
        headers['Content-Type'] = 'application/json'
        response = requests.post('http://127.0.0.1:5000/users/auth',
                                 data=json.dumps({"username": username,
                                                  "password": password}),
                                 headers=headers)
        return response

    def get_headers_authenticated_user(self):
        response = self.authenticate_user(self.username, self.password).json()

        headers = {}
        headers['Authorization'] = "Bearer " + response['access_token']
        headers['Content-Type'] = 'application/json'
        return headers

    # Test
    def test_catalog_api_get_all_items(self):
        response = self.app.get('/items')

        self.assertEqual(response.status_code, 200)

    def test_catalog_api_get_items_from_valid_category(self):
        response = self.app.get('/categories/1/items')

        self.assertEqual(response.status_code, 200)

    def test_catalog_api_get_items_from_invalid_category(self):
        response = self.app.get('/categories/2/items')

        self.assertEqual(response.status_code, 404)

    def test_catalog_api_get_item_from_invalid_category(self):
        response = self.app.get('/categories/2/items/1')

        self.assertEqual(response.status_code, 200)

    def test_catalog_api_create_new_item_valid(self):
        headers = self.get_headers_authenticated_user()
        json_data = {'title': 'Tacos2', 'description': 'My favorite tacos!'}
        response = self.app.post('/categories/1/items',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)

        self.assertEqual(response.status_code, 201)

    def test_catalog_api_create_new_item_invalid(self):
        headers = self.get_headers_authenticated_user()
        json_data = {'title': '', 'description': 'My favorite tacos!'}
        response = self.app.post('/categories/1/items',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)

        self.assertEqual(response.status_code, 422)

    def test_catalog_api_create_item_from_invalid_category(self):
        headers = self.get_headers_authenticated_user()
        json_data = {'title': 'Tacos2', 'description': 'My favorite tacos!'}
        response = self.app.post('/categories/2/items',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)

        self.assertEqual(response.status_code, 404)

    def test_catalog_create_item_with_no_input(self):
        headers = self.get_headers_authenticated_user()
        json_data = {}
        response = self.app.post('/categories/1/items',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)

        self.assertEqual(response.status_code, 400)

    def test_catalog_api_get_individual_item_valid(self):
        headers = self.get_headers_authenticated_user()
        response = self.app.get('/categories/1/items/1', headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hamburgers', json_data['item']['title'])
        self.assertIn('Classic dish elevated with pretzel buns.',
                      json_data['item']['description'])

    def test_catalog_api_get_individual_item_invalid(self):
        headers = self.get_headers_authenticated_user()
        response = self.app.get('/categories/1/items/5', headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('Item could not be found.', json_data['message'])

    def test_catalog_api_delete_item_valid(self):
        headers = self.get_headers_authenticated_user()
        response = self.app.delete('/categories/1/items/2',
                                   headers=headers,
                                   follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    def test_catalog_api_delete_item_invalid(self):
        headers = self.get_headers_authenticated_user()
        response = self.app.delete('/categories/1/items/16',
                                   headers=headers,
                                   follow_redirects=True)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('Item could not be found.', json_data['message'])

    def test_catalog_api_delete_item_from_invalid_category(self):
        headers = self.get_headers_authenticated_user()
        response = self.app.delete('/categories/2/items/1',
                                   headers=headers)

        self.assertEqual(response.status_code, 404)

    def test_catalog_api_delete_item_not_permited(self):
        response = self.authenticate_user('test', 'test123').json()

        headers = {}
        headers['Authorization'] = "Bearer " + response['access_token']
        headers['Content-Type'] = 'application/json'

        response = self.app.delete('/categories/1/items/1',
                                   headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 550)
        self.assertIn('Permission denied.', json_data['message'])

    def test_catalog_api_put_item_valid(self):
        headers = self.get_headers_authenticated_user()
        json_data = {'title': 'Updated item',
                     'description': 'My favorite item'}
        response = self.app.put('/categories/1/items/3',
                                data=json.dumps(json_data),
                                headers=headers,
                                follow_redirects=True)

        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated item successfully.', json_data['message'])

    def test_catalog_api_put_item_invalid(self):
        headers = self.get_headers_authenticated_user()
        json_data_input = {'title': 'Updated item',
                           'description': 'My favorite item'}
        response = self.app.put('/categories/1/items/15',
                                data=json.dumps(json_data_input),
                                headers=headers,
                                follow_redirects=True)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('Item could not be found.', json_data['message'])

    def test_catalog_api_put_item_not_permited(self):
        response = self.authenticate_user('test', 'test123').json()

        headers = {}
        headers['Authorization'] = "Bearer " + response['access_token']
        headers['Content-Type'] = 'application/json'

        json_data_input = {'title': 'Updated item',
                           'description': 'My favorite item'}
        response = self.app.put('/categories/1/items/1',
                                data=json.dumps(json_data_input),
                                headers=headers,
                                follow_redirects=True)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 550)
        self.assertIn('Permission denied.', json_data['message'])

    def test_catalog_api_put_item_from_invalid_category(self):
        headers = self.get_headers_authenticated_user()
        json_data = {'title': 'Tacos2', 'description': 'My favorite tacos!'}
        response = self.app.put('/categories/2/items/1',
                                data=json.dumps(json_data),
                                headers=headers,
                                follow_redirects=True)

        self.assertEqual(response.status_code, 404)

    def test_catalog_api_create_item_with_deleted_user(self):
        headers = self.get_headers_authenticated_user()
        current_user = UserModel.query.filter_by(username=self.username)\
            .first()
        db.session.delete(current_user)
        db.session.commit()

        json_data = {'title': 'Tacos', 'description': 'My favorite tacos!'}
        response = self.app.post('/categories/1/items',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)

        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('Invalid user.', json_data['message'])


if __name__ == "__main__":
    unittest.main()
