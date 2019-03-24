import unittest

import requests
from flask import json

from main import app, db
from main.models.user import UserModel
from main.libs.bcrypt_hash import generate_hash, verify_hash
from config import app_config
import main.controllers


class AuthenticateApiTests(unittest.TestCase):
    username = 'truongnt'
    password = '123456'

    # Executed prior to each tests
    def setUp(self):
        with app.app_context():
            app.config.from_object(app_config['testing'])
            self.app = app.test_client()
            db.drop_all()
            db.create_all()
            self.create_user()
            self.assertEqual(app.debug, False)

    # Executed after each tests
    def tearDown(self):
        with app.app_context():
            db.session.remove()

    # Helper methods
    def create_user(self):
        # Create a new user
        new_user = UserModel(self.username, generate_hash(self.password))
        db.session.add(new_user)
        db.session.commit()
        return

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
    def test_catalog_api_auth_invalid_user_password(self):
        headers = {}
        headers['Content-Type'] = 'application/json'
        response = self.app.post('http://127.0.0.1:5000/users/auth',
                                 data=json.dumps({"username": self.username,
                                                  "password": 'FlaskIsOk'}),
                                 headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('Wrong credentials.', json_data['message'])

    def test_catalog_api_auth_invalid_username(self):
        headers = {}
        headers['Content-Type'] = 'application/json'
        response = self.app.post('http://127.0.0.1:5000/users/auth',
                                 data=json.dumps({"username": 'Nobody',
                                                  "password": '123456'}),
                                 headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('Wrong credentials.', json_data['message'])

    def test_catalog_api_auth_valid_user(self):
        headers = {}
        headers['Content-Type'] = 'application/json'
        response = self.app.post('http://127.0.0.1:5000/users/auth',
                                 data=json.dumps({"username": self.username,
                                                  "password": self.password}),
                                 headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Logged in as {}.'.format(self.username),
                      json_data['message'])

    def test_catalog_api_register_invalid_user(self):
        headers = {'Content-Type': 'application/json'}
        json_data = {'username': 'truong123456', 'password': '123'}
        response = self.app.post('/users',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 422)

    def test_catalog_api_register_valid_user(self):
        headers = {'Content-Type': 'application/json'}
        json_data = {'username': 'truong123456', 'password': '123456xyz'}
        response = self.app.post('/users',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)
        self.assertEqual(response.status_code, 201)

    def test_catalog_api_register_existed_user(self):
        headers = {'Content-Type': 'application/json'}
        json_data = {'username': 'truongnt', 'password': '12345678'}
        response = self.app.post('/users',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('User already exists.', json_data['message'])

    def test_catalog_bcrypt_verify_hash(self):
        password = 'mypassword'
        hash = generate_hash(password)
        verify = verify_hash(hash, password)

        self.assertEqual(True, verify)

    def test_catalog_auth_invalid_token(self):
        token = "InvalidToken.invalid.invalid"
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }

        json_data = {
            'title': 'new title',
            'description': 'new description'
        }

        response = self.app.post('http://127.0.0.1:5000/categories/1/items',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)

        self.assertEqual(response.status_code, 400)

    def test_catalog_auth_invalid_header(self):
        headers = {}
        json_data = {
            'title': 'new title',
            'description': 'new description'
        }
        response = self.app.post('http://127.0.0.1:5000/categories/1/items',
                                 data=json.dumps(json_data),
                                 headers=headers,
                                 follow_redirects=True)

        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
