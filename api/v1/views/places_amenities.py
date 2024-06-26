#!/usr/bin/python3
"""
Module for handling RESTful API actions for the link between Place and Amenity objects.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, place, amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieve the list of all Amenity objects linked to a Place."""
    place = storage.get(place, place_id)
    if place is None:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Delete a Amenity object from a Place."""
    place = storage.get(place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(amenity, amenity_id)
    if amenity is None or amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Link a Amenity object to a Place."""
    place = storage.get(place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(amenity, amenity_id)
    if amenity is None:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
