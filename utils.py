import hashlib


def hash_password(password):
    """Return SHA-256 hash of a password."""
    return hashlib.sha256(password.encode()).hexdigest()


def line():
    print("=" * 50)