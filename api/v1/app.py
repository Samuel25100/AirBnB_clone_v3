#!/usr/bin/python3
"""Is where app instance of flask created"""
from models import storage
from flask import Flask, jsonify, request
import os
from api.v1.views import app_views


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

@app.errorhandler(404)
def error_404(error):
    return jsonify({"error": "Not found"}), 404

@app.teardown_appcontext
def teardown(error):
    storage.close()

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', '5000'), threaded=True)
