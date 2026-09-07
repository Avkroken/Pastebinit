# REPO.md

`Pastebinit` är ett Python-projekt med tester under `tests/` och Debian-paketering under `debian/`.

## Invarians

- `pyproject.toml` är källa till sanning för paketversionen.
- Versionen `MAJOR.MINOR.PATCH` ska matcha stabil release-tagg `vMAJOR.MINOR.PATCH`.

## GitHub-styrning

- Kanonisk arbets- och reviewpolicy finns i `Avkroken/.github/AGENTS.md`.
- `main` skyddas av det ärvda organisationsrulesetet `main` och repo-rulesetet `required-ci`.
- Required check på `main` är `python`.
- `dev` är integrationsgren när ett aktivt `dev-pilot`-ruleset finns. Lägg endast required status checks på `dev` när workflows bevisligen producerar exakt de check-namnen för PR mot `dev`.
- Organisationens CodeRabbit-UI är baslinje. Repository-lokal `.coderabbit.yaml` ska endast användas för uttryckligen repo-specifika overrides.

## Validering

- Läs `pyproject.toml`, berörda tester och relevanta Debian-filer innan relaterat beteende ändras.
- Kör relevanta pytest-, compile- och build-kontroller för den ändrade delen.
- När `debian/` eller Debian-paketgenerering ändras, kör förrådets Debian-validering.
