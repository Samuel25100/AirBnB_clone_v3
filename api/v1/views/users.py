#!/usr/bin/python3
"""handles all default RESTFul API actions for states"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    all_list = []
    all_users = storage.all(User).values()
    for i in all_users:
        all_list.append(i.to_dict())
    return all_list, 200


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def a_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return user.to_dict(), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return {}, 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    if request.is_json:
        val = request.get_json()
        if 'email' not in val:
            abort(400, description="Missing email")
        elif 'password' not in val:
            abort(400, description="Missing password")
        inst = User(**val)
        inst.save()
        return jsonify(inst.to_dict()), 201
    else:
        abort(404, description="Not a JSON")


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    elif request.is_json:
        ignore = ['id', 'email', 'created_at', 'updated_at']
        val = request.get_json()
        for key, value in val.items():
            if key not in ignore:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404, description="Not a JSON")
