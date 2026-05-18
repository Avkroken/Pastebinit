import json
import urllib.request
from .base import BasePastebin, PasteOptions, BackendError

_API = "https://paste.debian.net/api/v1/paste"

_EXPIRY_DAYS = {
    "N": 90, "1D": 1, "1W": 7, "2W": 14, "1M": 30, "6M": 90, "1Y": 90,
}


class PasteDebianNet(BasePastebin):
    name = "paste.debian.net"
    url = "https://paste.debian.net"
    supports_expiry = True
    supports_privacy = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        payload = json.dumps({
            "code": content,
            "filename": opts.title or "paste.txt",
            "expiry_days": _EXPIRY_DAYS.get(opts.expiry, 90),
            "private": opts.private > 0,
        }).encode()
        req = urllib.request.Request(_API, data=payload)
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "pastebinit/2.0.0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read())
        except OSError as e:
            raise BackendError(f"paste.debian.net error: {e}") from e
        if "error" in result:
            raise BackendError(f"paste.debian.net error: {result['error']}")
        return result.get("url", f"https://paste.debian.net/hidden/{result['id']}")
