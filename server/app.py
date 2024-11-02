"""App."""

from flask import Flask
from flask_cors import CORS

from server.config import get_config


def get_app():
    """Get app."""
    app = Flask(__name__)
    CORS(app, 
        resources={
            r"/*": {
                "origins": ["http://localhost:5173"],
                "methods": ["GET", "POST", "OPTIONS"],
                "supports_credentials": True,
                "expose_headers": ["Content-Range", "X-Content-Range", "X-USER-KEY"]
            }
        })
    app.config.from_object(get_config())
    return app
