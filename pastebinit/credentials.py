import base64
import json
import logging
import os
import stat
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "pastebinit"
KEYSTORE_FILE = CONFIG_DIR / "keystore"
logger = logging.getLogger(__name__)

_ENV_MAP: dict[str, dict[str, str]] = {
    "pastebin.com": {
        "api_dev_key": "PASTEBIN_API_KEY",
        "password": "PASTEBIN_PASSWORD",
        "username": "PASTEBIN_USERNAME",
    },
}


def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def _keyring_get(backend: str, field: str) -> Optional[str]:
    try:
        import keyring
        return keyring.get_password(f"pastebinit:{backend}", field)
    except Exception:
        return None


def _keyring_set(backend: str, field: str, value: str) -> bool:
    try:
        import keyring
        keyring.set_password(f"pastebinit:{backend}", field, value)
        return True
    except Exception:
        return False


def _keystore_get(backend: str, field: str, password: str) -> Optional[str]:
    if not KEYSTORE_FILE.exists():
        return None
    try:
        raw = KEYSTORE_FILE.read_bytes()
        salt, token = raw[:16], raw[16:]
        key = _derive_key(password, salt)
        decrypted = json.loads(Fernet(key).decrypt(token))
        return decrypted.get(backend, {}).get(field)
    except Exception:
        return None


def _keystore_set(backend: str, field: str, value: str, password: str) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    existing: dict = {}
    if KEYSTORE_FILE.exists():
        try:
            raw = KEYSTORE_FILE.read_bytes()
            salt_old, token = raw[:16], raw[16:]
            existing = json.loads(Fernet(_derive_key(password, salt_old)).decrypt(token))
        except Exception:
            logger.debug("Unable to read existing keystore; proceeding with new keystore content.", exc_info=True)
    salt = os.urandom(16)
    existing.setdefault(backend, {})[field] = value
    encrypted = Fernet(_derive_key(password, salt)).encrypt(json.dumps(existing).encode())
    # Create with 0600 from the start — write_bytes + chmod would leave a
    # window where the file is readable by other users.
    fd = os.open(KEYSTORE_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                 stat.S_IRUSR | stat.S_IWUSR)
    try:
        os.write(fd, salt + encrypted)
    finally:
        os.close(fd)
    KEYSTORE_FILE.chmod(stat.S_IRUSR | stat.S_IWUSR)


def get(backend: str, field: str) -> Optional[str]:
    """Return credential: env var → OS keyring → encrypted keystore."""
    env_key = _ENV_MAP.get(backend, {}).get(field)
    if env_key:
        val = os.environ.get(env_key)
        if val:
            return val

    val = _keyring_get(backend, field)
    if val:
        return val

    return None  # keystore requires explicit password prompt — call _keystore_get directly


def store(backend: str, field: str, value: str, password: str) -> None:
    """Store credential in keyring if available, else encrypted keystore."""
    if not _keyring_set(backend, field, value):
        _keystore_set(backend, field, value, password)


def clear(backend: str) -> bool:
    """Remove OS-keyring credentials for a backend. Returns True if anything was deleted."""
    deleted = False
    try:
        import keyring
        import keyring.errors
        for field in ("username", "user_key", "api_dev_key", "password"):
            try:
                keyring.delete_password(f"pastebinit:{backend}", field)
                deleted = True
            except keyring.errors.PasswordDeleteError:
                pass
    except Exception:
        pass
    return deleted
