#!/usr/bin/python3
"""handles all default RESTFul API actions for amenities"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    all_list = []
    all_state = storage.all(Amenity).values()
    for i in all_state:
        all_list.append(i.to_dict())
    return all_list, 200

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def a_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return amenity.to_dict(), 200

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        return {}, 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    if request.is_json:
        val = request.get_json()
        if 'name' not in val:
            abort(400, description="Missing name")
        inst = Amenity(**val)
        inst.save()
        return jsonify(inst.to_dict()), 201
    else:
        abort(404, description="Not a JSON")

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    elif request.is_json:
        ignore = ['id', 'created_at', 'updated_at']
        val = request.get_json()
        for key, value in val.items():
            if key not in ignore:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404, description="Not a JSON")
