# AGENTS.md

- Läs [README.md](README.md) och [docs/project-context.md](docs/project-context.md) före ändringar.
- Arkitektur och driftsverifiering finns i [docs/architecture.md](docs/architecture.md) och [docs/operations.md](docs/operations.md).
- Repositoryts egna README, `docs/`, AGENTS-instruktioner och versionerade konfiguration är auktoritativa för repositoryts tekniska arbete.
- Arbeta i separat gren enligt `{agent}/{feature}/{YYYY-MM-DD}/{HH-mm}-{id}`.
- Kör `pytest` efter relevanta ändringar.
- Bevara Python-stödgränsen och credentialmodell om uppgiften inte uttryckligen ändrar dem.
- Lägg aldrig credentials, keystore-innehåll eller andra hemligheter i repository eller dokumentation.
