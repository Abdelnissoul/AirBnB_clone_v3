#!/usr/bin/python3
"""
Module containing places_reviews views.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, review, place, user


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieve the list of all Review objects of a Place."""
    place = storage.get(place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/api/v1/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object."""
    review = storage.get(review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a Review."""
    place = storage.get(place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    user_id = data['user_id']
    user = storage.get(user, user_id)
    if user is None:
        abort(404)
    data['place_id'] = place_id
    review = review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/api/v1/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a Review object."""
    review = storage.get(review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200


@app_views.route('/api/v1/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object."""
    review = storage.get(review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200
