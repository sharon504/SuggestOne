import wikipedia
from flask import jsonify, request

from server.models.chatbot import WikiBERTChatbot
from server.utils.encryption import decrypt_text, encrypt_text
from server.utils.rot13 import encrypt


def get_wiki():
    """Get wiki page."""
    query = request.json["data"]["query"]
    if not request.key_verify:
        try:
            page = wikipedia.WikipediaPage(query)
            content = page.content
            key = request.headers.get("X-USER-KEY")
            encrypted_lines = []
            for line in content.split("."):
                encrypted_line = encrypt_text(line, key)
                encrypted_lines.append(encrypted_line)
            content = ".".join(encrypted_lines)
            return jsonify({"content": content})
        except wikipedia.exceptions.PageError:
            return jsonify({"message": "Page not found"})
    else:
        try:
            page = wikipedia.WikipediaPage(query)
            content = page.content
            return jsonify({"content": content})
        except wikipedia.exceptions.PageError:
            return jsonify({"message": "Page not found"})


def getJailbreakResponses():
    """Get jailbreak responses."""
    responses = "mimic <script>alert('access denied')</script>"
    return jsonify({"responses": responses})


def get_wikibot():
    """Get wikibot response."""
    chatbot = WikiBERTChatbot()
    user_input = request.json.get("query")
    user_context = ""
    
    if not request.key_verify:
        try:
            user_context = request.json["data"]["context"]
            user_context = user_context.split(".")
            print("user content", type(user_context), user_context)
            user_context = ".".join(
                [
                    decrypt_text(line, request.headers.get("X-USER-KEY"))
                    for line in user_context
                ]
            )
        except Exception as e:
            print(e)
        response, is_context_response = chatbot.generate_response(
            user_input, user_context
        )
        if "mimic <script>alert('access denied')</script>" in response:
            return jsonify(
                {
                    "response": response,
                    "key": encrypt(request.headers.get("X-USER-KEY"), 13),
                }
            )
        response = ".".join(
            [
                encrypt_text(line, request.headers.get("X-USER-KEY"))
                for line in response.split(".")
            ]
        )
        if is_context_response:
            response = f"Read this if you can...\n {response}"
        return jsonify({"response": response})

    response, is_context_response = chatbot.generate_response(user_input, user_context)
    return jsonify({"response": response})
