# AGENTS.md

- Läs [README.md](README.md) och [docs/project-context.md](docs/project-context.md) före ändringar.
- Arkitektur och driftsverifiering finns i [docs/architecture.md](docs/architecture.md) och [docs/operations.md](docs/operations.md).
- PR-titlar, SemVer och releasearbete följer [docs/release-standard.md](docs/release-standard.md); `pyproject.toml` äger package-versionen.
- Repositoryts egna README, `docs/`, AGENTS-instruktioner och versionerade konfiguration är auktoritativa för repositoryts tekniska arbete.
- Extern GitHub-governance är provider-state. Anta inte organization-scope eller andra org-funktioner utan live-verifiering.
- Arbeta i separat gren enligt `{agent}/{feature}/{date}`, där `date` skrivs som `YYYY-MM-DD`.
- Arbetet ska vara seriellt och semantiskt per repository: en arbetsgren/PR motsvarar en sammanhängande feature eller uppgift, och `feature`-delen ska beskriva arbetet semantiskt.
- Innan agenten påbörjar nästa uppgift i samma repository ska befintlig öppen arbetsgren, draft eller PR färdigställas genom relevanta checks, reviews och merge, eller uttryckligen avslutas/blockeras. Skapa inte tids-/ID-suffix eller parallella branchvarianter för att kringgå ett upptaget namn.
- Om `{agent}/{feature}/{date}` redan finns för uppgiften ska agenten fortsätta den befintliga arbetslinjen i stället för att skapa en ny.
- Commits ska använda Conventional Commits eller motsvarande tydlig typ, exempelvis `feat:`, `fix:`, `docs:`, `chore:`, `ci:` eller `test:`.
- Läs hela PR-review-state före merge, inklusive kommentarer och trådar som GitHub markerar som `outdated`; verifiera att grundproblemet faktiskt är löst.
- Kör `pytest` efter relevanta ändringar.
- Bevara Python-stödgränsen och credentialmodell om uppgiften inte uttryckligen ändrar dem.
- Lägg aldrig credentials, keystore-innehåll eller andra hemligheter i repository eller dokumentation.
## Agent skills

### Issue tracker

Use this repository's GitHub Issues for issues and specifications. Read `docs/agents/issue-tracker.md` before reading, creating, or publishing tickets.

### Domain docs

Use the single-context convention in `docs/agents/domain.md`; existing README, project-context, architecture, operations, and ADR documentation remain authoritative.

