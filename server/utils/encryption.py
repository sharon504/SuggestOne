import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from server.utils.rot13 import encrypt


def get_key_from_password(password, salt=None):
    password = encrypt(password, 13)
    if salt is None:
        salt = b"salt_"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def encrypt_text(text, password):
    key = get_key_from_password(password)
    cipher_suite = Fernet(key)

    encrypted_lines = []
    for line in text.split("\n"):
        encrypted_line = cipher_suite.encrypt(line.encode()).decode()
        encrypted_lines.append(encrypted_line)

    return "\n".join(encrypted_lines)


def decrypt_text(encrypted_text, password):
    key = get_key_from_password(password)
    cipher_suite = Fernet(key)

    decrypted_lines = []
    for line in encrypted_text.split("\n"):
        decrypted_line = cipher_suite.decrypt(line.encode()).decode()
        decrypted_lines.append(decrypted_line)

    return "\n".join(decrypted_lines)
