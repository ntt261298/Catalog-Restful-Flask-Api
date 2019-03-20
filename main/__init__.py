import os
from flask import Flask
from flask_jwt_extended import JWTManager

from main.authenticate.security import bcrypt
from database.db import db
from config import app_config

app = Flask(__name__)

jwt = JWTManager(app)

# Configurations
if os.environ['ENV'] not in ['development', 'production', 'testing']:
    app.config.from_object(app_config['default'])
else:
    app.config.from_object(app_config[os.environ['ENV']])


with app.app_context():
    db.init_app(app)
    bcrypt.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
