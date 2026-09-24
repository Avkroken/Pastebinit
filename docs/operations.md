# Drift och verifiering

## Utvecklingsmiljö

```bash
python -m pip install -e '.[test]'
```

Det installerar paketet editable tillsammans med testberoenden.

## Test

```bash
pytest
```

Testsviten täcker bland annat:

- CLI,
- config,
- credentials,
- syntaxdetektion,
- backendimplementationer,
- beroende-/workflowrelaterade repositoryinvariants.

## Snabb CLI-smoke

Efter ändringar i argumentparser eller packaging:

```bash
pastebinit --version
pastebinit --list-backends
pastebinit --help
```

Tester mot externa paste-tjänster ska inte ersätta hermetiska backendtester.

## Packaging

Verifiera att `pyproject.toml` fortsatt pekar på:

```text
pastebinit = pastebinit.cli:main
```

och att package discovery inkluderar `pastebinit*`.

Vid release-/packagingarbete bör en lokal build/install-smoke köras utöver pytest så att entrypoint och metadata verifieras.

## Configtest

Configtester ska använda isolerad config directory och inte operatörens riktiga `~/.config/pastebinit`.

## Credentialtest

Credentialtester får inte använda riktiga credentials. Testa:

- store/get/clear,
- krypterad/avsedd keystorehantering,
- login/logoutkontroll,
- fel vid saknad eller ogiltig auth.

## Backendförändringar

För varje ändrad backend, verifiera:

1. endpoint/requestdata;
2. capability flags;
3. response → URL parsing;
4. providerfel → normaliserat backendfel;
5. authspecifika paths när backenden stödjer auth.

## Releasegräns

Repositoryt är ett Python-paket. Releasearbete ska skiljas från vanlig PR-verifiering; tester ska inte implicit publicera paket.

## Felsökning

### Fel backend väljs

Kontrollera CLI-flagga, config default och registry.

### Funktion stöds inte

Kontrollera backendens capabilitydeklaration innan CLI-logik ändras.

### Loginproblem

Kontrollera först backendens authstöd, därefter credential store/keystore. Skriv inte ut sparade credentials för felsökning.

### Syntaxdetektion

Reproducera med samma input och filnamn och testa `pastebinit.syntax.detect` isolerat.
