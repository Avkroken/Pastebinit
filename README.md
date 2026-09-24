# pastebinit

`pastebinit` är ett Python-CLI för att skicka text och filer till flera paste-tjänster med gemensam syntax, automatisk syntaxdetektion och valfritt autentiserat backendstöd.

## Installation för utveckling

```bash
python -m pip install -e '.[test]'
pytest
```

Projektet kräver Python 3.10 eller senare.

## Exempel

Från stdin:

```bash
printf 'hello\n' | pastebinit
```

Från fil:

```bash
pastebinit example.py
```

Visa backendkapabiliteter:

```bash
pastebinit --list-backends
```

## Dokumentation

Börja i **[dokumentationsöversikten](docs/index.md)**.

- [Projektkontext](docs/project-context.md) — package, config och credentialmodell
- [Arkitektur](docs/architecture.md) — CLI → backend-abstraktion → HTTP-tjänst
- [Drift och verifiering](docs/operations.md) — utveckling, test och packaging
- [SECURITY.md](SECURITY.md) — säkerhetsrapportering

README hålls kort för att kommandoreferens och implementation inte ska blandas ihop med introduktionen.
