#!/usr/bin/python3
""" This script starts a Flask web application.
    Handles states using RESTful API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/api/v1/states', methods=['GET'],
                 strict_slashes=False)
def show_all_states():
    """ Retrieves and displays all State objects """
    new_list = []
    for x in storage.all('State').values():
        new_list.append(x.to_dict())

    return jsonify(new_list)


@app_views.route('/api/v1/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def show_specific_state(state_id):
    """ Retrieves and displays the State object by given
        state_id, if possible """
    state = storage.get('State', state_id)
    if state is not None:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Retrieves and deletes the State object by given
        state_id, if possible """
    result = storage.get('State', state_id)
    if result is not None:
        result.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/api/v1/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """ Creates a new State object """
    state = request.get_json()
    if state is None:
        abort(400, 'Not a JSON')
    if 'name' not in state:
        abort(400, 'Missing name')
    new_state = State(**state)
    storage.new(new_state)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/api/v1/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ Updates a State object by the given state_id,
        if possible """
    update_me = request.get_json()
    if update_me is None:
        abort(400, 'Not a JSON')
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    for key, value in update_me.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
