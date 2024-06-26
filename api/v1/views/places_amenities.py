#!/usr/bin/python3
"""handles all default RESTFul API actions for link Place and Amenity"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_place_amenities(place_id):
    all_list = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAG') == 'db':
        for i in place.amenities:
            all_list.append(i.to_dict())
    else:
        for i in place.amenity_ids:
            amenity = storage.get(Amenity, i)
            all_list.append(amenity.to_dict())
    return jsonify(all_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_places_amenities(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity_id not in place.amenity_ids:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAG') == 'db':
        place.amenities.remove(amenity)
    else:
        storage.delete(amenity)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_place_amenities(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        else:
            place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
