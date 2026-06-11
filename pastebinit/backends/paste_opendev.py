import urllib.parse
import urllib.request
from .base import BasePastebin, PasteOptions, BackendError, USER_AGENT


class PasteOpenDev(BasePastebin):
    name = "paste.opendev.org"
    url = "https://paste.opendev.org"
    supports_privacy = True
    supports_syntax = True

    def paste(self, content: str, opts: PasteOptions) -> str:
        fmt = opts.format if opts.format not in ("auto", "") else "text"
        params = {"code": content, "language": fmt}
        if opts.private > 0:
            params["private"] = "on"
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request("https://paste.opendev.org/", data=data)
        req.add_header("User-Agent", USER_AGENT)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.url
        except OSError as e:
            raise BackendError(f"paste.opendev.org error: {e}") from e
