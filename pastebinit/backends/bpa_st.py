import json
import urllib.request
from .base import BasePastebin, PasteOptions, BackendError, USER_AGENT

_API = "https://bpa.st/api/v1/paste"
# bpa.st currently only reliably supports "1day"; other values cause 400/500
_EXPIRY = {"1D": "1day"}


class BpaSt(BasePastebin):
    name = "bpa.st"
    url = "https://bpa.st"
    supports_expiry = True
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        lexer = opts.format if opts.format not in ("auto", "") else "text"
        payload = json.dumps({
            "files": [{"content": content, "lexer": lexer, "name": opts.title or "paste.txt"}],
            "expiry": _EXPIRY.get(opts.expiry, "1day"),
            "private": opts.private > 0,
        }).encode()
        req = urllib.request.Request(_API, data=payload)
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", USER_AGENT)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read())
        except OSError as e:
            raise BackendError(f"bpa.st error: {e}") from e
        if "link" not in result:
            raise BackendError(f"bpa.st error: unexpected response {result}")
        return result["link"]
