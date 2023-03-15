#!/usr/bin/env python3
'''basic flask app'''
from typing import Tuple, Union
from flask import Flask, jsonify, abort, request, redirect
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    '''basic flask app
    Returns:
        str: JSON payload
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> Tuple[str, int]:
    """Registers a new user if it does not exist before"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    response = {"email": email, "message": "user created"}
    return jsonify(response)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''implements login functionality
    Returns:
        str: JSON payload with session_id
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)

    if not valid_login:
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> Union[abort, redirect]:
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if session_id is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
