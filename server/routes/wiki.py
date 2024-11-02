from flask import Blueprint

from server.controllers.wiki_controller import (
    get_wiki,
    get_wikibot,
    getJailbreakResponses,
)
from server.middlewares.key_verify import key_verify

router = Blueprint("wiki", __name__, url_prefix="/")

key_valid = get_wiki
key_valid = key_verify(key_valid)

bot_valid = get_wikibot
bot_valid = key_verify(bot_valid)

router.add_url_rule("/", view_func=key_valid, methods=["POST"])
router.add_url_rule("/chat", view_func=bot_valid, methods=["POST"])
router.add_url_rule("/genBreakString", view_func=getJailbreakResponses, methods=["GET"])
