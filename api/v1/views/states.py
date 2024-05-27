#!/usr/bin/python3
"""handles all default RESTFul API actions for states"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    all_list = []
    all_state = storage.all(State).values()
    for i in all_state:
        all_list.append(i.to_dict())
    return jsonify(all_list)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def a_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    if request.is_json:
        val = request.get_json()
        if 'name' not in val:
            abort(400, description="Missing name")
        inst = State(**val)
        inst.save()
        return jsonify(inst.to_dict()), 201
    else:
        abort(404, description="Not a JSON")

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    elif request.is_json:
        ignore = ['id', 'created_at', 'updated_at']
        val = request.get_json()
        for key, value in val.items():
            if key not in ignore:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict())
    else:
        abort(404, description="Not a JSON")
