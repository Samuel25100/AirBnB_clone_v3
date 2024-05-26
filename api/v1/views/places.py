#!/usr/bin/python3
"""handles all default RESTFul API actions for Place"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def state_places(city_id):
    all_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for i in city.places:
        all_list.append(i.to_dict())
    return jsonify(all_list), 200

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def a_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return {}, 200

@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.is_json:
        val = request.get_json()
        if 'user_id' not in val:
            abort(400, description="Missing user_id")
        user = storage.get(User, val.user_id)
        if user is None:
            abort(404)
        if 'name' not in val:
            abort(400, description="Missing name")        
        val["city_id"] = city_id
        inst = Place(**val)
        inst.save()
        return jsonify(inst.to_dict()), 201
    else:
        abort(404, description="Not a JSON")


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    elif request.is_json:
        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        val = request.get_json()
        for key, value in val.items():
            if key not in ignore:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404, description="Not a JSON")
