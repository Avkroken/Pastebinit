# AGENTS.md

- Läs [README.md](README.md) och [docs/project-context.md](docs/project-context.md) före ändringar.
- Arkitektur och driftsverifiering finns i [docs/architecture.md](docs/architecture.md) och [docs/operations.md](docs/operations.md).
- PR-titlar, SemVer och releasearbete följer [docs/release-standard.md](docs/release-standard.md); `pyproject.toml` äger package-versionen.
- Repositoryts egna README, `docs/`, AGENTS-instruktioner och versionerade konfiguration är auktoritativa för repositoryts tekniska arbete.
- Extern GitHub-governance är provider-state. Anta inte organization-scope eller andra org-funktioner utan live-verifiering.
- Arbeta i separat gren enligt `{agent}/{feature}/{YYYY-MM-DD}`.
- Commits ska använda Conventional Commits eller motsvarande tydlig typ, exempelvis `feat:`, `fix:`, `docs:`, `chore:`, `ci:` eller `test:`.
- Läs hela PR-review-state före merge, inklusive kommentarer och trådar som GitHub markerar som `outdated`; verifiera att grundproblemet faktiskt är löst.
- Kör `pytest` efter relevanta ändringar.
- Bevara Python-stödgränsen och credentialmodell om uppgiften inte uttryckligen ändrar dem.
- Lägg aldrig credentials, keystore-innehåll eller andra hemligheter i repository eller dokumentation.
