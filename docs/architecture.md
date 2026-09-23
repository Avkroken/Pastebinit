# Arkitektur

## Översikt

```text
stdin / file / CLI args
        |
        v
 pastebinit.cli
        |
        +--> config
        +--> credential resolution
        |
        v
 selected backend adapter
        |
        v
 pastebin service
        |
        v
 returned paste URL/result
```

## Lager

- **CLI** — argumenttolkning, input och användarflöde.
- **Backend adapters** — tjänstespecifik request/response-hantering.
- **Configuration** — användar- och backendinställningar.
- **Credentials** — environment/keyring och krypterad fallback.
- **Packaging** — setuptools via `pyproject.toml`.

## Säkerhetsgräns

Backendcredentials är lokal användarstate. De ska inte loggas, inkluderas i felmeddelanden eller checkas in.

Fallback-keystoren är en säkerhetsmekanism, inte en bekvämlighetscache. Ändringar där ska bevara autentiserad kryptering och restriktiva filrättigheter.

## Extensibility

Nya backends ska isolera tjänstespecifik logik och inte läcka specialfall in i generisk CLI-/credentialkod om det kan undvikas.
