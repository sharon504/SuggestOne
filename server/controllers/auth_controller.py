"""Auth controller."""

import uuid

from flask import jsonify, request

from server.app import get_app

app = get_app()


def get_key():
    """Get key."""
    key = str(uuid.uuid4())
    return jsonify({"key": key})


def is_key_valid():
    """Check if key is valid."""
    if request.key_verify:
        return jsonify({"valid": True})
    return jsonify({"valid": False})
