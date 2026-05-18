from unittest.mock import patch
from tests.conftest import make_http_response
from pastebinit.backends.paste_opendev import PasteOpenDev
from pastebinit.backends.base import PasteOptions


def test_paste_returns_url():
    mock = make_http_response("", url="https://paste.opendev.org/show/abc/")
    with patch("urllib.request.urlopen", return_value=mock):
        url = PasteOpenDev().paste("hello\nworld\ntest", PasteOptions())
    assert url == "https://paste.opendev.org/show/abc/"


def test_paste_sends_form_fields():
    mock = make_http_response("", url="https://paste.opendev.org/show/abc/")
    with patch("urllib.request.urlopen", return_value=mock) as m:
        PasteOpenDev().paste("hello", PasteOptions(format="python", private=1))
    req = m.call_args[0][0]
    body = req.data.decode()
    assert "language=python" in body
    assert "private=on" in body
