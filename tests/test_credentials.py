import os
from unittest.mock import patch


def test_get_from_env_var(tmp_path):
    with patch.dict(os.environ, {"PASTEBIN_API_KEY": "testkey123"}):
        from pastebinit import credentials
        result = credentials.get("pastebin.com", "api_dev_key")
        assert result == "testkey123"


def test_get_returns_none_when_nothing_configured(tmp_path):
    clean_env = {k: v for k, v in os.environ.items()
                 if k not in ("PASTEBIN_API_KEY", "PASTEBIN_PASSWORD", "PASTEBIN_USERNAME")}
    with patch.dict(os.environ, clean_env, clear=True), \
         patch("pastebinit.credentials.KEYSTORE_FILE", tmp_path / "keystore"), \
         patch("pastebinit.credentials._keyring_get", return_value=None):
        from pastebinit import credentials
        result = credentials.get("pastebin.com", "api_dev_key")
        assert result is None


def test_store_and_retrieve_from_keystore(tmp_path):
    ks = tmp_path / "keystore"
    with patch("pastebinit.credentials.KEYSTORE_FILE", ks), \
         patch("pastebinit.credentials.CONFIG_DIR", tmp_path), \
         patch("pastebinit.credentials._keyring_get", return_value=None), \
         patch("pastebinit.credentials._keyring_set", return_value=False):
        from pastebinit import credentials
        credentials._keystore_set("pastebin.com", "api_dev_key", "secretkey", "mypassword")
        assert ks.exists()
        assert oct(ks.stat().st_mode)[-3:] == "600"
        result = credentials.get(
            "pastebin.com", "api_dev_key", keystore_password="mypassword"
        )
        assert result == "secretkey"


def test_keystore_is_not_read_without_explicit_password(tmp_path):
    ks = tmp_path / "keystore"
    with patch("pastebinit.credentials.KEYSTORE_FILE", ks), \
         patch("pastebinit.credentials.CONFIG_DIR", tmp_path), \
         patch("pastebinit.credentials._keyring_get", return_value=None):
        from pastebinit import credentials
        credentials._keystore_set("pastebin.com", "api_dev_key", "secretkey", "mypassword")
        assert credentials.get("pastebin.com", "api_dev_key") is None


def test_wrong_password_returns_none(tmp_path):
    ks = tmp_path / "keystore"
    with patch("pastebinit.credentials.KEYSTORE_FILE", ks), \
         patch("pastebinit.credentials.CONFIG_DIR", tmp_path):
        from pastebinit import credentials
        credentials._keystore_set("pastebin.com", "pw", "value", "correct")
        result = credentials.get("pastebin.com", "pw", keystore_password="wrong")
        assert result is None


def test_wrong_password_does_not_replace_existing_keystore(tmp_path):
    import pytest
    from pastebinit import credentials
    ks = tmp_path / "keystore"
    with patch.object(credentials, "KEYSTORE_FILE", ks), patch.object(credentials, "CONFIG_DIR", tmp_path):
        credentials._keystore_set("first", "user_key", "original", "correct")
        original = ks.read_bytes()
        with pytest.raises(ValueError):
            credentials._keystore_set("second", "user_key", "new", "wrong")
        assert ks.read_bytes() == original
        assert credentials._keystore_get("first", "user_key", "correct") == "original"


def test_failed_keystore_replace_preserves_existing_file(tmp_path):
    import pytest
    from pastebinit import credentials
    ks = tmp_path / "keystore"
    with patch.object(credentials, "KEYSTORE_FILE", ks), patch.object(credentials, "CONFIG_DIR", tmp_path):
        credentials._keystore_set("first", "user_key", "original", "correct")
        original = ks.read_bytes()
        with patch("os.replace", side_effect=OSError("synthetic write failure")):
            with pytest.raises(OSError):
                credentials._keystore_set("second", "user_key", "new", "correct")
        assert ks.read_bytes() == original
        assert list(tmp_path.iterdir()) == [ks]


def test_successful_keystore_update_preserves_other_credentials(tmp_path):
    from pastebinit import credentials
    ks = tmp_path / "keystore"
    with patch.object(credentials, "KEYSTORE_FILE", ks), patch.object(credentials, "CONFIG_DIR", tmp_path):
        credentials._keystore_set("first", "user_key", "original", "correct")
        credentials._keystore_set("second", "user_key", "new", "correct")
        assert credentials._keystore_get("first", "user_key", "correct") == "original"
        assert credentials._keystore_get("second", "user_key", "correct") == "new"
        assert ks.stat().st_mode & 0o777 == 0o600
