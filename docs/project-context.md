# Projektkontext

**Senast verifierad:** 2026-09-24

## Ansvar

pastebinit är ett Python-paket och CLI för att skicka text eller filer till paste-tjänster via en gemensam command-line interface.

## Packaging

`pyproject.toml` definierar:

- package name: `pastebinit`
- Python: `>=3.10`
- build backend: setuptools
- CLI entrypoint: `pastebinit = pastebinit.cli:main`
- runtime dependencies för credential/configstöd
- optional test dependencies med pytest och PyYAML.

## CLI

`pastebinit/cli.py` stöder bland annat:

- filer eller stdin,
- backendval,
- title,
- syntax/format,
- privacy,
- expiry,
- backendmappar där de stöds,
- echo/verbose,
- login/logout,
- listning av backendkapabiliteter.

## Config

Konfiguration ligger under:

```text
$XDG_CONFIG_HOME/pastebinit/config.toml
```

eller motsvarande `~/.config/pastebinit/config.toml` när `XDG_CONFIG_HOME` inte är satt.

Verifierade defaults:

- backend: `bpa.st`
- privacy: `1`
- expiry: `N`
- format: `auto`

## Backendmodell

Varje backend implementerar den gemensamma kontraktytan i `pastebinit/backends/base.py` och annonserar capabilities som auth, folders, expiry, privacy och syntax.

CLI:t ska inte anta att alla backends stödjer samma funktioner.

## Credentials

Login är backendberoende. Sparade credentials är skilda från vanlig config och ska hanteras genom repositoryts credentialmodul/keystoremodell.

Secrets eller autentiseringsvärden hör aldrig hemma i testfixtures, README eller docs.

## Syntaxdetektion

När formatet är `auto` används `pastebinit.syntax.detect` med innehåll och filnamn som underlag.

## Kompatibilitet

Python 3.10+ är packagekontraktet. För Python före 3.11 används `tomli`; 3.11+ använder standardbibliotekets `tomllib`.

## Dokumentationsgräns

Detta dokument beskriver repositoryts publika kod och packagekontrakt, inte organisationsspecifik governance.

## Uppdateringskontrakt

Uppdatera dokumentationen när CLI-kontrakt, backendlista/capabilities, configformat, credentialmodell, Python-version eller packaging ändras.
