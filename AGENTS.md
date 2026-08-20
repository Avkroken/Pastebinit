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

## Arbetsflöde: exakt en uppgift åt gången

Repositoryt har exakt två arbetsgrenar: `dev` och `main`. Skapa aldrig en tredje gren, inte ens tillfälligt. Allt utvecklingsarbete görs på `dev` och går via ett ändringsförslag från `dev` till `main`.

En agent får ha exakt en aktiv koduppgift åt gången. Flera uppgifter är en kö, inte parallellt arbete. Nästa uppgift får inte påbörjas förrän den aktuella uppgiften är mergad eller uttryckligen blockerad av något agenten inte kan lösa själv.

Arbeta lokalt så långt det är praktiskt innan du pushar. Samla sammanhängande ändringar, testfixar och följdjusteringar i meningsfulla batcher i stället för att pusha varje liten edit och därmed starta om CI i onödan. När en PR redan kör CI får du fortsätta analysera, testa och förbättra samma uppgift lokalt. Push endast när du har en ny sammanhängande batch som faktiskt behöver valideras. CI-väntan är aldrig ett skäl att börja på nästa uppgift.

För varje uppgift:

1. Synka `dev` med `main`. Om `dev` redan innehåller ofärdigt arbete, slutför det först.
2. Implementera och testa den aktuella uppgiften lokalt på `dev`; samla ändringar i så stora sammanhängande batcher som är rimliga.
3. Commit och push till `dev`, skapa eller uppdatera exakt ett PR `dev` → `main`, och aktivera auto-merge.
4. Medan CI/review pågår: fortsätt endast lokalt med samma uppgift. Lös relevanta fel och kommentarer och pusha dem samlat, inte en i taget.
5. När PR:n är mergad, synka `dev` till `main`. Först därefter får nästa uppgift börja.

Om uppgiften blockeras av en extern åtgärd som agenten faktiskt inte kan utföra, dokumentera den exakta blockeraren och stanna. Börja inte en annan koduppgift utan uttrycklig instruktion från användaren.

## Tillåtet
- Ändra kod på `dev`
- Köra lokala tester och analyser
- Öppna ändringsförslag endast från `dev` till `main`
- Rätta CI- och reviewproblem för den aktiva uppgiften tills PR:n kan mergas

## Förbjudet
- Skapa andra grenar än `dev` och `main`
- Arbeta parallellt på flera koduppgifter
- Börja nästa uppgift medan den aktuella PR:n fortfarande är öppen eller blockerad
- Skicka ändringar direkt till `main` eller `master`
- Radera grenar
- Stänga av arbetsflöden
- Ändra hemligheter
- Ändra inställningar för GitHub-organisationen
- Tvinga igenom en push eller kringgå branch protection/rulesets

## Krav
- Överlämna kodändringar endast på `dev`
- Alla relevanta tester måste godkännas
- Håll varje ändringsförslag avgränsat till en uppgift
- Arbeta lokalt så mycket som möjligt och undvik onödigt täta pushar som startar om CI
- Ta aldrig med orelaterade ändringar
- Överlämna aldrig inloggningsuppgifter eller andra hemligheter till versionshistoriken
- Skapa ändringsförslag som klara för granskning, aldrig som utkast
- Aktivera automatisk sammanfogning med en metod som tillåts av förrådets regler direkt efter att ändringsförslaget skapats
- Automatisk sammanfogning får slutföras först när alla regelkrav och kontrollkörningar har godkänts
- Om CI, review eller auto-merge blockerar leveransen: lös blockeraren för den aktiva uppgiften innan annat kodarbete påbörjas
- Om automatisk sammanfogning inte kan aktiveras: rapportera det exakta felet
- Efter merge: synka `dev` till `main` innan nästa uppgift

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
