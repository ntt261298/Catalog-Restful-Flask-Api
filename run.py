from main import app
import main.controllers
from main.authenticate.security import bcrypt
from database.db import db


@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)
bcrypt.init_app(app)

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True, host='0.0.0.0')
