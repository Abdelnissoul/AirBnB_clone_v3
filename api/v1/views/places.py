#!/usr/bin/python3
"""
Module containing places views.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, place, city, user


@app_views.route('/api/v1/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieve the list of all Place objects of a City."""
    city = storage.get(city, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/api/v1/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object."""
    place = storage.get(place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/api/v1/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a Place."""
    city = storage.get(city, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user_id = data['user_id']
    user = storage.get(user, user_id)
    if user is None:
        abort(404)
    data['city_id'] = city_id
    place = place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/api/v1/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update a Place object."""
    place = storage.get(place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/api/v1/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object."""
    place = storage.get(place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200
