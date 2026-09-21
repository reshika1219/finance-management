import hashlib
import os


def hash_pin(pin: str, salt: bytes = None) -> tuple[str, str]:
    """
    Hashes a 4-digit PIN using PBKDF2-HMAC-SHA256.
    Returns (hex_hash, hex_salt).
    """
    if not is_valid_pin_format(pin):
        raise ValueError("PIN must be exactly 4 numeric digits.")

    if salt is None:
        salt = os.urandom(16)

    hash_bytes = hashlib.pbkdf2_hmac("sha256", pin.encode("utf-8"), salt, 100_000)
    return hash_bytes.hex(), salt.hex()


def verify_pin(pin: str, hex_hash: str, hex_salt: str) -> bool:
    """
    Verifies a user-entered PIN against the stored hash and salt.
    """
    if not is_valid_pin_format(pin):
        return False

    try:
        salt = bytes.fromhex(hex_salt)
        calc_hash, _ = hash_pin(pin, salt)
        return calc_hash == hex_hash
    except Exception:
        return False


def is_valid_pin_format(pin: str) -> bool:
    """
    Checks if a PIN consists of exactly 4 numeric digits.
    """
    if not pin or len(pin) != 4:
        return False
    return pin.isdigit()
