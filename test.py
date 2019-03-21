# Project/test.py
import unittest

import requests
from flask import json

from main import app, db
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel
from config import app_config
import main.controllers


class CatalogApiTests(unittest.TestCase):
    username = 'truongnt'
    password = '123456'
    cat_name = 'Cat1'

    # Executed prior to each test
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

    # Executed after each test
    def tearDown(self):
        pass

    # Helper methods
    def create_users(self):
        # Create a new user 
        new_user = UserModel(self.username, self.password)
        new_user.save_to_db()
        return

    def create_categories(self):
        # Create a new category
        new_category = CategoryModel(self.cat_name)
        new_category.save_to_db()
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
        headers = {}
        headers['Content-Type'] = 'application/json'
        response = requests.post('http://127.0.0.1:5000/users/auth',
                                 data=json.dumps({"username": self.username,
                                                  "password": self.password}),
                                 headers=headers).json()
        headers = {}
        headers['Authorization'] = "Bearer " + response['access_token']
        headers['Content-Type'] = 'application/json'
        return headers

    # Test
    def test_catalog_api_auth_invalid_user(self):
        response = self.authenticate_user(self.username, 'FlaskIsOK')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Wrong credentials.', response.json()['message'])

    def test_catalog_api_auth_valid_user(self):
        response = self.authenticate_user(self.username, self.password)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Logged in as {}.'.format(self.username),
                      response.json()['message'])

    def test_catelog_api_register_invalid_user(self):
        headers = {'Content-Type': 'application/json'}
        json_data = {'username': 'truong123456', 'password': '123'}
        response = self.app.post('/users',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 422)

    def test_catelog_api_register_valid_user(self):
        headers = {'Content-Type': 'application/json'}
        json_data = {'username': 'truong123456', 'password': '123456xyz'}
        response = self.app.post('/users',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 201)

    def test_catalog_api_invalid_token(self):
        headers = {}
        token = 'InvalidTokenInvalidToken'
        auth = 'Bearer ' + token
        headers['Authorization'] = auth
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        response = self.app.post('/users/items', headers=headers)

        self.assertEqual(response.status_code, 405)

    def test_catalog_api_get_all_categories(self):
        response = self.app.get('/items')

        self.assertEqual(response.status_code, 200)

    def test_catalog_api_get_all_items(self):
        response = self.app.get('/items')

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

    def test_catalog_api_get_user_items_valid(self):
        headers = self.get_headers_authenticated_user()
        response = self.app.get('/users/items',
                                headers=headers)

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
