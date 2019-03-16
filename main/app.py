from flask import Flask
from flask_jwt import JWT
from main.libs.security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Turn off Flask Track

app.secret_key = 'truong'
jwt = JWT(app, authenticate, identity)  # auth


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from database.db import db

    db.init_app(app)
    app.run(port=5000, debug=True, threaded=True, host='0.0.0.0')
