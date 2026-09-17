import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from jose import jwt


# ============================================================
# PASSWORD SECURITY
# ============================================================

ALGORITHM = "sha256"
ITERATIONS = 310000
SALT_LENGTH = 16


def hash_password(password: str) -> str:
    """
    Securely hash a password using PBKDF2-HMAC-SHA256.

    Stored format:
    pbkdf2_sha256$iterations$salt$hash
    """

    if not isinstance(password, str):
        raise ValueError("Password must be a string.")

    if not password:
        raise ValueError("Password cannot be empty.")

    salt = secrets.token_bytes(SALT_LENGTH)

    password_bytes = password.encode("utf-8")

    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt,
        ITERATIONS
    )

    return (
        "pbkdf2_sha256$"
        + str(ITERATIONS)
        + "$"
        + salt.hex()
        + "$"
        + derived_key.hex()
    )


def verify_password(
    plain_password: str,
    stored_password: str
) -> bool:
    """
    Verify a password against a stored PBKDF2 hash.
    """

    try:

        parts = stored_password.split("$")

        if len(parts) != 4:
            return False

        algorithm = parts[0]
        iterations = int(parts[1])
        salt = bytes.fromhex(parts[2])
        stored_hash = bytes.fromhex(parts[3])

        if algorithm != "pbkdf2_sha256":
            return False

        password_bytes = plain_password.encode("utf-8")

        derived_key = hashlib.pbkdf2_hmac(
            "sha256",
            password_bytes,
            salt,
            iterations
        )

        return hmac.compare_digest(
            derived_key,
            stored_hash
        )

    except Exception:

        return False


# ============================================================
# COMPATIBILITY HELPERS
# ============================================================

def get_password_hash(password: str) -> str:

    return hash_password(password)


def verify_password_hash(
    password: str,
    password_hash: str
) -> bool:

    return verify_password(
        password,
        password_hash
    )


# ============================================================
# JWT CONFIGURATION
# ============================================================

SECRET_KEY = "INTERVIEWIQ_DEMO_SECRET_KEY_CHANGE_IN_PRODUCTION"

JWT_ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


# ============================================================
# CREATE ACCESS TOKEN
# ============================================================

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    """
    Create a JWT access token.
    """

    payload = data.copy()

    if expires_delta is None:

        expires_delta = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    expire = (
        datetime.now(timezone.utc)
        + expires_delta
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


# ============================================================
# DECODE ACCESS TOKEN
# ============================================================

def decode_access_token(
    token: str
):
    """
    Decode and validate a JWT access token.
    """

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                JWT_ALGORITHM
            ]
        )

        return payload

    except Exception:

        return None