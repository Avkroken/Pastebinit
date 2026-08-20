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

## Tillåtet
- Ändra kod
- Köra tester
- Öppna ändringsförslag från `dev` till standardgrenen

## Förbjudet
- Skicka ändringar direkt till `main` eller `master`
- Radera grenar
- Stänga av arbetsflöden
- Ändra hemligheter
- Ändra inställningar för GitHub-organisationen

## Krav
- Överlämna kodändringar endast på `dev`
- Alla tester måste godkännas
- Håll varje ändringsförslag avgränsat till en uppgift
- Ta aldrig med orelaterade ändringar
- Överlämna aldrig inloggningsuppgifter eller andra hemligheter till versionshistoriken
- Tvinga aldrig igenom en skickning
- Skapa ändringsförslag som klara för granskning, aldrig som utkast
- Aktivera automatisk sammanfogning med en sammanfogningsöverlämning direkt efter att ändringsförslaget skapats
- Automatisk sammanfogning får slutföras först när alla regelkrav och kontrollkörningar har godkänts
- Om automatisk sammanfogning inte kan aktiveras: rapportera det exakta felet

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
