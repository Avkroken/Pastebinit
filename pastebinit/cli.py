import argparse
import getpass
import os
import sys
from typing import Optional

import sentry_sdk

from pastebinit import __version__
from pastebinit.backends import get_backend, BACKENDS, DEFAULT_BACKEND
from pastebinit.backends.base import PasteOptions, BackendError, AuthError, NotSupportedError
from pastebinit import config as cfg
from pastebinit import credentials
from pastebinit.credentials import KEYSTORE_FILE
from pastebinit.syntax import detect


def build_parser() -> argparse.ArgumentParser:
    defaults = cfg.load()
    p = argparse.ArgumentParser(
        prog="pastebinit",
        description="Send text and files to pastebin services.",
    )
    p.add_argument("files", nargs="*", metavar="FILE", help="Files to paste (default: stdin)")
    p.add_argument("-b", "--backend", default=cfg.get_default("backend", defaults),
                   metavar="NAME", help=f"Backend to use (default: {DEFAULT_BACKEND})")
    p.add_argument("-t", "--title", default="", metavar="TEXT", help="Paste title")
    p.add_argument("-f", "--format", default=cfg.get_default("format", defaults),
                   metavar="FMT", help="Syntax format (default: auto-detect)")
    p.add_argument("-p", "--private", type=int, default=cfg.get_default("private", defaults),
                   choices=[0, 1, 2], metavar="0-2",
                   help="Privacy: 0=public 1=unlisted 2=private")
    p.add_argument("-e", "--expiry", default=cfg.get_default("expiry", defaults),
                   metavar="CODE", help="Expiry: N 10M 1H 1D 1W 2W 1M 6M 1Y")
    p.add_argument("--folder", metavar="NAME", help="Upload to folder (pastebin.com)")
    p.add_argument("--create-folder", action="store_true",
                   help="Create folder if it does not exist")
    p.add_argument("-E", "--echo", action="store_true", help="Print content to stdout too")
    p.add_argument("-V", "--verbose", action="store_true", help="Verbose output to stderr")
    p.add_argument("-u", "--username", metavar="USER", help="Username override")
    p.add_argument("--login", action="store_true", help="Login and save credentials")
    p.add_argument("--logout", action="store_true", help="Clear saved credentials")
    p.add_argument("-l", "--list-backends", action="store_true",
                   help="List all backends with capabilities")
    p.add_argument("--version", action="version", version=f"pastebinit {__version__}")
    return p


def _yn(v: bool) -> str:
    return "yes" if v else "no"


def _print_backends():
    header = f"{'Backend':<22} {'Auth':^4} {'Folders':^7} {'Expiry':^6} {'Privacy':^7} {'Syntax':^6}"
    print(header)
    print("-" * len(header))
    for name, cls in sorted(BACKENDS.items()):
        b = cls()
        print(f"{name:<22} {_yn(b.supports_auth):^4} {_yn(b.supports_folders):^7} "
              f"{_yn(b.supports_expiry):^6} {_yn(b.supports_privacy):^7} {_yn(b.supports_syntax):^6}")


def run(args: argparse.Namespace) -> Optional[str]:
    if args.list_backends:
        _print_backends()
        return None

    backend = get_backend(args.backend)

    if args.login:
        username = args.username or input(f"Username for {args.backend}: ")
        password = getpass.getpass(f"Password for {args.backend}: ")
        try:
            user_key = backend.login(username, password)
            pw = getpass.getpass("Keystore password (to encrypt credentials): ")
            credentials.store(args.backend, "username", username, pw)
            credentials.store(args.backend, "user_key", user_key, pw)
            print(f"Logged in to {args.backend} successfully.")
        except (AuthError, NotSupportedError) as e:
            print(f"Login failed: {e}", file=sys.stderr)
            sys.exit(1)
        return None

    if args.logout:
        deleted = credentials.clear(args.backend)
        if deleted:
            print(f"Credentials for {args.backend} cleared.")
        else:
            print(f"No stored credentials found for {args.backend}.")
            if KEYSTORE_FILE.exists():
                print(f"Note: encrypted keystore at {KEYSTORE_FILE} may still contain credentials.")
        return None

    filenames = args.files or ["-"]
    last_url = None

    for filename in filenames:
        if filename == "-":
            content = sys.stdin.read().rstrip()
            display_name = None
        else:
            try:
                with open(filename) as f:
                    content = f.read().rstrip()
                display_name = filename
            except OSError as e:
                print(f"Cannot read {filename}: {e}", file=sys.stderr)
                sys.exit(1)

        if not content:
            print("Nothing to paste — input is empty.", file=sys.stderr)
            sys.exit(1)

        fmt = args.format
        if fmt == "auto":
            fmt = detect(content, filename=display_name)

        if args.echo:
            print(content)

        user_key = getattr(args, "user_key", None) or credentials.get(args.backend, "user_key")

        opts = PasteOptions(
            title=args.title or (display_name or ""),
            format=fmt,
            private=args.private,
            expiry=args.expiry,
            folder=args.folder,
            create_folder=args.create_folder,
            user_key=user_key,
        )

        if args.verbose:
            print(f"Pasting to {args.backend} (format={fmt}, private={args.private})",
                  file=sys.stderr)

        try:
            url = backend.paste(content, opts)
        except BackendError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        if args.echo:
            print("-" * len(url))
        print(url)
        last_url = url

    return last_url


def main():
    dsn = os.getenv("SENTRY_DSN")
    if dsn:
        sentry_sdk.init(dsn=dsn, traces_sample_rate=1.0, send_default_pii=False)

    parser = build_parser()
    args = parser.parse_args()
    try:
        run(args)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise
