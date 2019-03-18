from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

jwt = JWTManager(app)

# Configurations
app.config.from_object('config')
