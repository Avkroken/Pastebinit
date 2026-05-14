# pastebinit — Claude Code Guide

A command-line tool for sending text and files to pastebin services. Originally a Launchpad project, now maintained here with Python packaging.

## Tech Stack

- Python ≥ 3.10
- setuptools / pyproject.toml
- `cryptography`, `keyring` for credential storage
- pytest for tests

## Dev Commands

```bash
pip install -e ".[dev]"     # Install in editable mode with dev deps
pastebinit --help           # Run CLI
pytest                      # Run tests
```

## Project Structure

```
pastebinit/         # Main package
  cli.py            # CLI entrypoint
tests/              # pytest tests
pyproject.toml      # Package metadata and build config
```

## Conventions

- Entry point: `pastebinit.cli:main`
- Conventional Commits for releases (release-please)
- Never hardcode credentials — use keyring
- Tests live in `tests/` and must pass before merging
