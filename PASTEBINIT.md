# PASTEBINIT.md

This is the repository governance document for `Avkroken/Pastebinit`. Binding AI coding-agent policy is defined only in `Avkroken/.github/AGENTS.md`. This document records repository-specific technical contracts, invariants, validation requirements, and operational context required by that policy; it must not define, supplement, narrow, or override agent policy.

## Repository

`pastebinit` is a Python project with its test suite under `tests/` and Debian packaging under `debian/`.

## Validation

- Read `pyproject.toml`, the affected tests and Debian packaging files before changing related behavior.
- Run the relevant pytest, compile/build and packaging checks for the changed area.
- When `debian/` or the release flow changes, validate Debian packaging as part of the change.

## GitHub Actions contract

- `.github/workflows/ci.yml` owns the `python` check context and performs the repository's Python verification.
- `.github/workflows/release.yml` invokes the SHA-pinned Release Please workflow from `Avkroken/.github`. The Release PR updates `CHANGELOG.md`, `pyproject.toml`, the release manifest and the marked Debian package version before passing normal repository merge gates.
- `release-please-config.json` and `.release-please-manifest.json` are the release automation contract. `pyproject.toml` is the Python package version source; its version must match the stable `vMAJOR.MINOR.PATCH` release tag.
- The marked top stanza in `debian/changelog` follows the same upstream version for Debian package metadata. User-facing release history belongs in `CHANGELOG.md`, not in the rolling Debian metadata stanza.
- `.github/workflows/release-deb.yml` runs automatically for a published stable GitHub Release and remains manually retryable with an existing tag. It verifies both Python and Debian versions before building and uploads missing amd64/arm64 `.deb` assets to that release.
- Pin third-party GitHub Actions to full commit SHAs.
