# pastebinit — AI Agent Guide

A command-line tool for sending text and files to pastebin services. Originally a Launchpad project, now maintained here with Python packaging.

## Tech Stack

- Python ≥ 3.10
- setuptools / pyproject.toml
- `cryptography`, `keyring` for credential storage
- pytest for tests

## Dev Commands

```bash
pip install -e ".[dev]"          # Install in editable mode with dev deps
pastebinit --help                # Run CLI
pytest                           # Run tests
dpkg-buildpackage -b -us -uc    # Build .deb locally (output in repo root)
```

## Project Structure

```
pastebinit/         # Main package
  cli.py            # CLI entrypoint
tests/              # pytest tests
debian/             # Debian packaging (control, rules, changelog)
pyproject.toml      # Package metadata and build config
```

## Debian Packaging

- `debian/control` — `Architecture: any` produces per-arch packages (amd64, arm64)
- `debian/rules` — overrides `dh_builddeb` to copy the `.deb` into the repo root after build
- Built with `dpkg-buildpackage -b -us -uc`; `DEB_BUILD_OPTIONS=nocheck` skips tests in CI
- Output: `pastebinit_<version>-1_<arch>.deb` in the repo root

## Release Process

Merging to `main` triggers `auto-release.yml` automatically:

1. **tag** — bumps patch version, creates git tag
2. **build-deb** (matrix) — builds in parallel on `ubuntu-latest` (amd64) and `ubuntu-24.04-arm` (arm64)
3. **release** — creates GitHub release and attaches both `.deb` files

To manually rebuild a `.deb` for an existing tag, use `workflow_dispatch` in `build.yml`.

## Conventions

- Entry point: `pastebinit.cli:main`
- Conventional Commits — patch/minor/major bumps drive automatic versioning
- Never hardcode credentials — use keyring
- Tests live in `tests/` and must pass before merging
- `.deb` and build artifacts are gitignored — never commit them

## Allowed
- Committa på dev
- Modify code
- Run tests
- Open PRs

## Forbidden
- Push directly to main/master
- Merge PRs
- Skapa eller ta bort grenar (rulesetet blockerar det)
- Disable workflows
- Modify secrets
- Change GitHub org settings

## Requirements
- All tests must pass
- Keep PRs focused
- Never include unrelated changes
- Never commit credentials
- Never force push

## Svarsformat

Regeluppsättningen kommer från plugin:et `i-have-adhd`. Den laddas inte i
alla sessioner (t.ex. inte i Claude Code på webben), så den står här —
det här är källan som gäller oavsett var agenten kör.

Form:

- Led med åtgärden eller kommandot, inte med bakgrunden
- Numrera flerstegsprocesser, ett avgränsat steg per rad
- Max fem punkter per lista
- Hoppa över inledningar, sammanfattningar och avslutningsfraser
- Långa förklaringar bara på begäran

Innehåll:

- Säg uttryckligen vad som är gjort och vad som återstår
- Ange konkreta tidsuppskattningar
- Visa vad som fungerar efter en ändring, inte bara att den är gjord
- Vid fel: var, varför och hur det åtgärdas — kortfattat
- Avsluta med ett nästa steg som tar under två minuter
