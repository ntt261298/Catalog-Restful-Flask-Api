from flask import Flask
from flask_jwt_extended import JWTManager
<<<<<<< HEAD
=======
from main.authenticate.security import bcrypt
from database.db import db
>>>>>>> test

app = Flask(__name__)

jwt = JWTManager(app)

# Configurations
app.config.from_object('config')
<<<<<<< HEAD
=======

jwt = JWTManager(app)


with app.app_context():
    db.init_app(app)
    bcrypt.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()



>>>>>>> test
