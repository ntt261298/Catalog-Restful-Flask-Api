import os

from flask import Flask
from flask_jwt_extended import JWTManager

from main.libs.database import db
from config import app_config

app = Flask(__name__)

jwt = JWTManager(app)

# Configurations
try:
    if os.environ['ENV'] in ['development', 'production', 'testing']:
        app.config.from_object(app_config[os.environ['ENV']])
    else:
        app.config.from_object(app_config['default'])
except Exception:
    app.config.from_object(app_config['default'])

with app.app_context():
    db.init_app(app)
