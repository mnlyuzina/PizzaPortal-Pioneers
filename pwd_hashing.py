import hashlib


def hashing(password):
    hash_pwd = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hash_pwd