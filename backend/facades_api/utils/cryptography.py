"""
Cryptography functions are defined here.
"""

from hashlib import shake_128


def hash_password(email: str, password: str) -> str:
    """
    Hash given password with email used as salt.
    """
    return shake_128(f"{email[:(len(email) >> 1)]}{password}{email[(len(email) >> 1):]}".encode()).hexdigest(64)
