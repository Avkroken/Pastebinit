# Drift och verifiering

## Lokal utveckling

```bash
python -m pip install -e '.[test]'
pytest
```

## Packagingkontroll

Verifiera vid ändringar i packaging:

- att `pyproject.toml` är giltig,
- att CLI entrypoint fortfarande installerar `pastebinit`,
- att Python 3.10-gränsen inte ändras oavsiktligt,
- att runtime-dependencies matchar importer i paketet.

## Credentialtester

Vid ändringar i auth/credentialkod ska verifiering täcka:

- environment-baserad credentialkälla,
- OS-keyring när tillgänglig,
- krypterad fallback när keyring saknas,
- att känsliga värden inte skrivs i klartext eller logg,
- att fallbackfilens restriktiva rättigheter bevaras.

## Backendtester

Nätverksberoende tester ska inte göra repositoryts grundverifiering beroende av en extern pastebin-tjänsts tillgänglighet när beteendet kan testas med mocks/fixtures.

## Releasegräns

Versionsnummer och publik kompatibilitet definieras i `pyproject.toml`. Dokumentationen ska uppdateras när CLI-beteende eller supportgränser förändras.
