from flask import Blueprint

from server.controllers.auth_controller import get_key, is_key_valid
from server.middlewares.key_verify import key_verify

router = Blueprint("auth", __name__, url_prefix="/auth")

key_valid = is_key_valid
key_valid = key_verify(key_valid)

router.add_url_rule("/key", view_func=get_key, methods=["GET"])
router.add_url_rule("/regenkey", view_func=get_key, methods=["GET"])
router.add_url_rule("/key/valid/", view_func=key_valid, methods=["POST"])
