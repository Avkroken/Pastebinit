# pastebinit

`pastebinit` skickar text och filer till pastebin-tjänster från kommandoraden.

## Krav

- Python 3.10 eller senare
- Valfri OS-keyring för säker lagring av autentiseringsuppgifter

## Installation

```bash
python -m pip install .
```

För utveckling och test:

```bash
python -m pip install -e '.[test]'
pytest
```

## Användning

Skicka stdin till standard-backend:

```bash
printf 'hello\n' | pastebinit
```

Skicka en fil till en viss backend:

```bash
pastebinit --backend bpa.st fil.txt
```

Visa tillgängliga backends och funktioner:

```bash
pastebinit --list-backends
```

Se alla flaggor:

```bash
pastebinit --help
```

## Autentisering och credentials

För backends med inloggning används i första hand miljövariabler och därefter operativsystemets keyring.

```bash
pastebinit --backend pastebin.com --login
```

Om OS-keyring inte är tillgänglig lagras credentials i den krypterade filen `~/.config/pastebinit/keystore`. CLI:n frågar då efter keystore-lösenordet när den behöver läsa den sparade autentiseringen. Lösenordet lagras inte i klartext av `pastebinit`.

Den krypterade fallback-keystoren skapas med filrättighet `0600` och använder PBKDF2-HMAC-SHA256 samt Fernet för kryptering/autentisering.

## Konfiguration

Användarkonfiguration lagras under XDG-konfigurationskatalogen, normalt `~/.config/pastebinit/`.

## Test

```bash
pytest
```

## Licens

GPL-2.0-or-later.
