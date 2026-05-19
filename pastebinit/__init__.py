from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("pastebinit")
except PackageNotFoundError:
    __version__ = "unknown"
