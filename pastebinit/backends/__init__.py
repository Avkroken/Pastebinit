from .pastebin_com import PastebinCom
from .dpaste import DPaste
from .paste_debian_net import PasteDebianNet
from .paste_ubuntu_com import PasteUbuntuCom
from .paste_opendev import PasteOpenDev
from .bpa_st import BpaSt

BACKENDS: dict[str, type] = {
    "pastebin.com": PastebinCom,
    "dpaste.com": DPaste,
    "paste.debian.net": PasteDebianNet,
    "paste.ubuntu.com": PasteUbuntuCom,
    "paste.opendev.org": PasteOpenDev,
    "bpa.st": BpaSt,
}

DEFAULT_BACKEND = "bpa.st"


def get_backend(name: str):
    """Return instantiated backend by name, raise ValueError if unknown."""
    cls = BACKENDS.get(name)
    if cls is None:
        known = ", ".join(sorted(BACKENDS))
        raise ValueError(f"Unknown backend '{name}'. Known backends: {known}")
    return cls()
