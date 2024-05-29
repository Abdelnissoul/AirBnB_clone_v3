#!/usr/bin/python3
"""
Module containing states views.
It takes the modules from state and storage 
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, State


@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve the list of all State objects."""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/api/v1/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieve a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/api/v1/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a State."""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Update a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200
