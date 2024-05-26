#!/usr/bin/python3
"""handles all default RESTFul API actions for City"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def state_cities(state_id):
    all_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for i in state.cities:
        all_list.append(i.to_dict())
    return jsonify(all_list), 200

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def a_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return {}, 200

@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.is_json:
        val = request.get_json()
        if 'name' not in val:
            abort(400, description="Missing name")
        inst = City(**val)
        inst.state_id = state.id
        inst.save()
        return jsonify(inst.to_dict()), 201
    else:
        abort(404, description="Not a JSON")


@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    elif request.is_json:
        ignore = ['id', 'state_id', 'created_at', 'updated_at']
        val = request.get_json()
        for key, value in val.items():
            if key not in ignore:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404, description="Not a JSON")
