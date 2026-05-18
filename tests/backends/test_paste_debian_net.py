import json
import pytest
from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.paste_debian_net import PasteDebianNet
from pastebinit.backends.base import PasteOptions, BackendError


@pytest.fixture
def backend():
    return PasteDebianNet()


def test_paste_returns_url(backend):
    body = json.dumps({"id": "abc123", "url": "https://paste.debian.net/hidden/abc123"})
    mock = make_http_response(body)
    with patch("urllib.request.urlopen", return_value=mock):
        url = backend.paste("hello\nworld\ntest", PasteOptions())
    assert url == "https://paste.debian.net/hidden/abc123"


def test_paste_sends_json(backend):
    body = json.dumps({"id": "abc123", "url": "https://paste.debian.net/hidden/abc123"})
    mock = make_http_response(body)
    with patch("urllib.request.urlopen", return_value=mock) as m:
        backend.paste("hello\nworld\ntest", PasteOptions(format="python"))
    req = m.call_args[0][0]
    payload = json.loads(req.data)
    assert payload["code"] == "hello\nworld\ntest"


def test_paste_error_raises(backend):
    body = json.dumps({"error": "No code provided"})
    mock = make_http_response(body)
    with patch("urllib.request.urlopen", return_value=mock):
        with pytest.raises(BackendError):
            backend.paste("hello", PasteOptions())
