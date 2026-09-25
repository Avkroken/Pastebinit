# Dokumentation

Navigationssida för pastebinit.

## Hitta rätt

| Behov | Dokument |
| --- | --- |
| förstå package, konfiguration och kompatibilitet | [Projektkontext](project-context.md) |
| förstå CLI-, backend- och credentialgränser | [Arkitektur](architecture.md) |
| utveckla, testa och verifiera paketet | [Drift](operations.md) |
| versionera och skapa releases | [Release- och versionsstandard](release-standard.md) |
| rapportera säkerhetsproblem | [SECURITY.md](../SECURITY.md) |

## Funktionella områden

### CLI

`pastebinit/cli.py` hanterar argument, stdin/filer, syntaxval, privacy/expiry, login/logout och backendval.

### Backends

`pastebinit/backends/` innehåller den gemensamma backendabstraktionen och konkreta implementationer för de tjänster repositoryt stöder.

Aktuella backendmoduler omfattar bland annat:

- bpa.st
- dpaste
- paste.debian.net
- paste.opendev.org
- paste.ubuntu.com
- pastebin.com

Använd `pastebinit --list-backends` för aktuell capability-matris i runtime.

### Config

`pastebinit/config.py` använder TOML under XDG config directory och har defaults för backend, privacy, expiry och syntax.

### Credentials

Autentiseringsuppgifter hanteras separat från vanlig config. Loginflödet kan lagra credentials i avsedd credential store/keystore; credentials ska aldrig dokumenteras eller läggas i repositoryt.

## Ändringskarta

- nya CLI-flaggor → README vid användarsynlig funktion + architecture
- ny backend → backendtest + architecture
- configformat/defaults → project-context
- credentials/login → architecture + credentialtester
- packaging/Python-version → project-context + operations + release-standard
- release/PR-title/SemVer → release-standard

## Wiki

Om GitHub Wiki används kan den ge klickbar användar- och backenddokumentation. Versionsstyrda docs är underlaget för teknisk current-state; aktuell Wiki-setting är extern GitHub-state.
