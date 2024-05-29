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


@app_views.route('/api/v1/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """Search for places based on JSON request body."""
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    places = set()
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            places.update(state.places)
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            places.update(city.places)

    if amenities:
        filtered_places = []
        for place in places:
            place_amenities = {amenity.id for amenity in place.amenities}
            if set(amenities).issubset(place_amenities):
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])


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
