# Arkitektur

## Översikt

```text
stdin / files
     |
     v
pastebinit.cli
     |
     +--> config
     +--> syntax detection
     +--> credentials
     |
     v
backend registry
     |
     v
selected Backend
     |
     v
remote paste service
     |
     v
returned URL
```

## CLI-lager

`pastebinit.cli` är användarkontraktet. Det:

1. laddar defaults från config;
2. parser argument;
3. väljer backend;
4. läser filer eller stdin;
5. auto-detekterar syntax vid behov;
6. bygger `PasteOptions`;
7. anropar backendens `paste()`;
8. skriver resulterande URL.

## Backendabstraktion

`pastebinit/backends/base.py` separerar CLI:t från leverantörsspecifika HTTP-kontrakt.

Varje backend kan ha olika stöd för:

- authentication,
- folders,
- expiry,
- privacy,
- syntax.

CLI och tester ska därför använda deklarerade capabilities i stället för att hårdkoda ett gemensamt featureantagande.

## Registry

`pastebinit/backends/__init__.py` exponerar registrerade backends och default backend. Nya backendimplementationer ska registreras där och få egna tester.

## Config

Vanliga användarinställningar lagras som TOML. Config innehåller defaults, inte känsliga credentials.

## Credential boundary

Credentials hanteras av `pastebinit.credentials` och är separerade från den vanliga TOML-konfigurationen.

Loginflödet:

1. frågar backend efter login/user key där auth stöds;
2. tar keystore-lösenord separat;
3. lagrar användarnamn/user key genom credentialmodulen.

Logout rensar backendens sparade credentialposter enligt modulens kontrakt.

## Inputmodell

CLI:t behandlar `-` som stdin. Övriga argument läses som filer. Tom input avvisas.

Flera filer kan skickas i samma invocation och behandlas sekventiellt.

## Felmodell

Backend-specifika failures normaliseras genom backend exceptions. Auth- eller unsupported-funktioner ska ge tydliga CLI-fel i stället för traceback som normal användarupplevelse.

## Extensibility

En ny backend ska minst:

1. implementera backendkontraktet;
2. deklarera capabilities korrekt;
3. registreras;
4. ha isolerade tester för request/response och errors;
5. inte flytta leverantörsspecifik logik in i CLI:t.
