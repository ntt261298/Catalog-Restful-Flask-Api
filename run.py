from main import app
import main.controllers


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    from database.db import db
    db.init_app(app)
    app.run(port=5000, debug=True, threaded=True, host='0.0.0.0')
