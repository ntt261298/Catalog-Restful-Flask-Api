from flask import Flask
from flask_jwt_extended import JWTManager
import main.controllers
from main.authenticate.security import bcrypt
from database.db import db

app = Flask(__name__)

# Configurations
app.config.from_object('config')


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)
db.init_app(app)
bcrypt.init_app(app)
