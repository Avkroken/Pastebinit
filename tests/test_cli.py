import sys
import argparse
import pytest
from io import StringIO
from unittest.mock import patch, MagicMock
from pastebinit.cli import build_parser, run, _load_user_key


@pytest.fixture(autouse=True)
def no_real_config(tmp_path):
    """Isolate all CLI tests from real config files."""
    with patch("pastebinit.config.CONFIG_FILE", tmp_path / "config.toml"):
        yield


def test_parser_defaults():
    parser = build_parser()
    args = parser.parse_args([])
    assert args.backend == "bpa.st"
    assert args.private == 1
    assert args.expiry == "N"
    assert args.format == "auto"


def test_parser_backend_flag():
    parser = build_parser()
    args = parser.parse_args(["-b", "pastebin.com"])
    assert args.backend == "pastebin.com"


def test_parser_list_backends():
    parser = build_parser()
    args = parser.parse_args(["-l"])
    assert args.list_backends is True


def test_run_from_stdin_returns_url(tmp_path):
    fake_stdin = StringIO("hello world")
    mock_backend = MagicMock()
    mock_backend.paste.return_value = "https://bpa.st/ABCD"
    with patch("sys.stdin", fake_stdin), \
         patch("pastebinit.cli.get_backend", return_value=mock_backend):
        args = argparse.Namespace(
            backend="bpa.st", files=[], title="", format="auto",
            private=1, expiry="N", folder=None, create_folder=False,
            echo=False, verbose=False, login=False, logout=False,
            username=None, list_backends=False, user_key=None,
        )
        url = run(args)
    assert url == "https://bpa.st/ABCD"


def test_load_user_key_prompts_for_existing_keystore(tmp_path):
    args = argparse.Namespace(backend="pastebin.com", user_key=None)
    backend = MagicMock(supports_auth=True)
    calls = []

    def fake_get(backend_name, field, keystore_password=None):
        calls.append((backend_name, field, keystore_password))
        return "stored-key" if keystore_password == "unlock" else None

    with patch("pastebinit.cli.KEYSTORE_FILE", tmp_path / "keystore") as keystore, \
         patch("pastebinit.cli.credentials.get", side_effect=fake_get), \
         patch("pastebinit.cli.getpass.getpass", return_value="unlock"):
        keystore.write_text("encrypted")
        assert _load_user_key(args, backend) == "stored-key"

    assert calls == [
        ("pastebin.com", "user_key", None),
        ("pastebin.com", "user_key", "unlock"),
    ]


def test_version_flag(capsys):
    with pytest.raises(SystemExit):
        build_parser().parse_args(["--version"])
