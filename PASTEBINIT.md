# PASTEBINIT.md

Repository-specific instructions for `Avkroken/Pastebinit`. These instructions supplement the canonical Avkroken policy in `Avkroken/.github/AGENTS.md`.

## Repository

`pastebinit` is a Python project with its test suite under `tests/` and Debian packaging under `debian/`. The manual `.deb` release workflow is separate from pull-request CI.

## Validation

- Read `pyproject.toml`, the affected tests and Debian packaging files before changing related behavior.
- Run the relevant pytest, compile/build and packaging checks for the changed area.
- When `debian/` or the release flow changes, validate Debian packaging as part of the change.

## GitHub Actions contract

- `.github/workflows/ci.yml` owns the `python` check context and performs the repository's Python verification.
- `.github/workflows/release-deb.yml` is a manual release job for an already existing tag and must remain separate from pull-request CI.
- Pin third-party GitHub Actions to full commit SHAs.
