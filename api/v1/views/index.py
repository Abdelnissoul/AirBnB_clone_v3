#!/usr/bin/python3
"""Index module to handle the /status route."""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status')
def api_status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """gets the stats by calling stats"""
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }

    return jsonify(stats)