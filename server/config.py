import os
from datetime import timedelta


class BaseConfig:
    """Base configuration class with common settings."""

    # Flask Core Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
    JSON_SORT_KEYS = False

    CORS_HEADERS = "Content-Type"

    COOKIE_EXPIRE = timedelta(minutes=30)
    # JWT Settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    TESTING = False


config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig,
}


def get_config():
    """Helper function to get configuration class based on environment."""
    env = os.getenv("FLASK_ENV", "default")
    return config[env]
