from hashlib import sha256


def encrypt(raw_text: str):
    return sha256(raw_text.encode("utf-8")).hexdigest()
