from flask import Flask
from flask_jwt_extended import JWTManager
from main.authenticate.security import bcrypt
from database.db import db

app = Flask(__name__)

jwt = JWTManager(app)

# Configurations
app.config.from_object('config')


with app.app_context():
    db.init_app(app)
    bcrypt.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()




