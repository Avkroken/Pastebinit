import json
from unittest.mock import patch
import pytest
from tests.conftest import make_http_response
from pastebinit.backends.bpa_st import BpaSt
from pastebinit.backends.base import PasteOptions, BackendError


def test_paste_returns_url():
    body = json.dumps({"link": "https://bpa.st/ABCD", "removal": "https://bpa.st/remove/XYZ"})
    mock = make_http_response(body, url="https://bpa.st/ABCD")
    with patch("urllib.request.urlopen", return_value=mock):
        url = BpaSt().paste("hello\nworld\ntest", PasteOptions())
    assert url == "https://bpa.st/ABCD"


def test_paste_sends_json():
    body = json.dumps({"link": "https://bpa.st/ABCD", "removal": ""})
    mock = make_http_response(body)
    with patch("urllib.request.urlopen", return_value=mock) as m:
        BpaSt().paste("hello\nworld\ntest", PasteOptions(format="python"))
    req = m.call_args[0][0]
    payload = json.loads(req.data)
    assert payload["files"][0]["lexer"] == "python"
    assert payload["expiry"] == "1day"


def test_paste_error_raises():
    body = json.dumps({"error": "bad request"})
    mock = make_http_response(body)
    with patch("urllib.request.urlopen", return_value=mock):
        with pytest.raises(BackendError):
            BpaSt().paste("hello", PasteOptions())
