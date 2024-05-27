#!/usr/bin/python3
"""handles all default RESTFul API actions for City"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    all_list = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for i in place.reviews:
        all_list.append(i.to_dict())
    return jsonify(all_list)

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def a_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.is_json:
        val = request.get_json()
        if 'user_id' not in val:
            abort(400, description="Missing user_id")
        elif storage.get(User, user_id) is None:
            abort(404)
        if 'text' not in val:
            abort(400, description="Missing text")
        val['place_id'] = place.id
        inst = Review(**val)
        inst.save()
        return jsonify(inst.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    elif request.is_json:
        ignore = ['id', 'place_id', 'user_id','created_at', 'updated_at']
        val = request.get_json()
        for key, value in val.items():
            if key not in ignore:
                setattr(city, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(400, description="Not a JSON")
