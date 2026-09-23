# Projektkontext

**Senast verifierad:** 2026-09-23

## Ansvar

`pastebinit` är ett Python-CLI för att skicka text och filer till flera pastebin-backends.

Packaging och CLI-kontrakt definieras i `pyproject.toml`:

- package: `pastebinit`
- version: `2.4.6`
- Python: `>=3.10`
- CLI entrypoint: `pastebinit = pastebinit.cli:main`
- license: GPL-2.0-or-later

## Dependencies

Runtime:

- `cryptography`
- `keyring`
- `tomli-w`
- `tomli` för Python < 3.11

Test-extra:

- `pytest`
- `pyyaml`

## Credentialmodell

Credential-resolution ska prioritera runtime/environment där sådan backendkonfiguration finns och därefter OS-keyring.

När OS-keyring inte går att använda finns en lokal krypterad fallback-keystore under XDG-konfigurationskatalogen. Den får inte degraderas till klartextlagring.

## Konfigurationsgräns

Användarkonfiguration hör hemma under XDG config, normalt `~/.config/pastebinit/`. Repositoryt ska inte innehålla användarspecifika credentials eller lokala keystore-filer.

## Kompatibilitet

Central Python CI ska bevara projektets deklarerade stödgräns från Python 3.10 och uppåt. Versionsändringar i `requires-python` är en publik kompatibilitetsändring och ska behandlas som sådan.

## Uppdateringskontrakt

Uppdatera denna fil när CLI entrypoint, Python-stöd, credentialmodell, backendmodell eller packaging ändras.
