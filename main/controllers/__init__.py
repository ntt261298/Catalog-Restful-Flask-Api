from flask import jsonify

import category
import item
import user
from main import app


@app.errorhandler(404)
def not_found():
    return jsonify({"message": "Not found."}), 404


@app.errorhandler(405)
def method_not_allowed():
    return jsonify({"message": "Method not allowed."}), 405


@app.errorhandler(Exception)
def method_not_allowed(e):
    return jsonify({"message": "Something went wrong."}), 500
