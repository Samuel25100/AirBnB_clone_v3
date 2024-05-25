#!/usr/bin/python3
"""Index file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', strict_slashes=False)
def status():
    """Status output"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def stat():
    """retrieves the number of each objects by type"""
    cls = ['Amenity','City','Place', 'Review', 'State','User']
    key = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    dic = {}
    for i in range(0, 6):
        val = storage.count(cls[i])
        dic[key[i]] = val
    return jsonify(dic)
