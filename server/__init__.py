from flask import Flask
from flask_cors import CORS


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    from server.config import get_config
    from server.routes import auth, wiki

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

    app.register_blueprint(auth.router)
    app.register_blueprint(wiki.router)
    return app
