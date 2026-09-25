# Release- och versionsstandard

**Senast verifierad:** 2026-09-25

Det här dokumentet gäller **Avkroken/Pastebinit**. Repositoryts egna filer är source of truth för package-, release- och versionskontraktet.

## Nuvarande version och canonical källa

Pastebinit är ett Python-paket byggt med setuptools.

Canonical package-version är:

```toml
[project]
version = "2.4.6"
```

i `pyproject.toml`.

Det finns ingen root `CHANGELOG.md` på current `main` och ingen verifierad aktuell Release Please-/`action-gh-release`-workflow. Äldre PR-historik får inte användas som current-state för releaseautomation.

Inför inte `version.txt` eller en andra manuellt underhållen versionskälla. En framtida releaseautomation ska uppdatera den befintliga `[project].version`.

## PR-titlar och squash commits

Pull request-titlar ska följa Conventional Commits:

```text
<type>[optional scope][!]: <description>
```

Tillåtna typer:

- `feat` — ny funktion;
- `fix` — buggfix;
- `perf` — prestandaförändring;
- `refactor` — beteendebevarande omstrukturering;
- `docs` — dokumentation;
- `test` — tester;
- `build` — build-/paketeringssystem;
- `ci` — CI/CD;
- `chore` — underhåll utan produktfunktion;
- `revert` — återställning av tidigare förändring.

Scope är valfri och kan exempelvis vara `cli`, `backends`, `credentials` eller `deps`.

`!` markerar breaking change:

```text
feat(cli)!: replace argument contract
```

Workflow `.github/workflows/pr-title.yml` validerar titeln på `pull_request`. Det använder inga secrets, checkar inte ut kod och har `permissions: {}`.

Aktuella Dependabot-PR:er använder redan kompatibla titlar som `chore(deps): ...`.

## SemVer

När en versionerad release skapas gäller:

- breaking change → **major**;
- `feat` → normalt **minor**;
- `fix` → normalt **patch**;
- `docs`, `test`, `chore`, `ci` och `build` → normalt ingen version ensamma;
- `perf` och `refactor` bedöms efter faktisk användar-/paketeffekt.

Versionsnumret i `pyproject.toml` ska representera paketets release, inte antalet deployments eller merges.

## När en release ska ske

Release sker kuraterat, inte på varje merge.

En release är motiverad när:

- användarsynlig funktionalitet är färdig;
- en buggfix bör få en officiell versionspunkt;
- ett breaking CLI-/backend-/configkontrakt behöver en tydlig major-release;
- flera färdiga ändringar ska samlas till en begriplig package-release.

GitHub Releases är den avsedda officiella releasehistoriken för Portalens Changelog.

## Release-PR-målbild

Målflödet är:

```text
main changes
  -> Conventional Commit-historik
  -> release-PR
  -> pyproject.toml version + release notes
  -> pytest + package/build smoke + relevanta repositorychecks
  -> merge
  -> tag
  -> GitHub Release
```

Package-publicering till extern registry är **inte verifierad current state** och ingår inte automatiskt bara för att en GitHub Release skapas.

## Verifiering vid release

Utöver vanlig PR-CI ska release-/packagingarbete verifiera:

```bash
python -m pip install -e '.[test]'
pytest
pastebinit --version
pastebinit --list-backends
pastebinit --help
```

Vid faktisk package-build ska en build/install-smoke göras så att package metadata och CLI-entrypoint verifieras. Ingen test eller release-PR ska implicit publicera paketet.

## Releaseautomation — current state

Automatisk release-PR/taggning är inte verifierad som aktiv på current `main`.

Release Please är tekniskt kompatibelt med Conventional Commits och har Python-releasehantering som kan uppdatera den befintliga package-versionen. Det är däremot **inte aktiverat här**.

Den normala Release Please Actions-modellen med repositoryts `GITHUB_TOKEN` har en blocker: PR:er/taggar skapade av den tokenen triggar inte efterföljande GitHub Actions-workflows. En release-PR skulle då inte automatiskt få samma Python-/dependency-verifiering som vanliga PR:er.

Upstreamreferens: `https://github.com/googleapis/release-please-action#other-actions-on-release-please-prs`.

Följande används inte som genväg:

- ny PAT utan separat credentialbeslut;
- bredare GitHub App-writebehörighet för en befintlig read-only integration;
- lättade CI-/review-/repositoryskydd;
- merge av release-PR utan relevant verifiering.

Full releaseautomation förblir blockerad tills ett least-privilege write-identitetsflöde eller en annan CI-kompatibel modell uttryckligen är vald.

## CHANGELOG

Det finns ingen root `CHANGELOG.md` på current `main`.

GitHub Releases används därför som releasehistorik i nuvarande modell. En framtida releaseautomation kan införa versionsstyrd changelog **som del av samma release-PR**, men då ska den genereras från canonical commit/releasehistorik och inte bli en separat manuellt underhållen sanning.

Debian-`debian/changelog` är packaginghistorik och ska inte behandlas som ersättning för repositoryts övergripande releasehistorik.

## Prereleases

Prereleases används endast när det finns ett konkret distributionsbehov. Använd SemVer-suffix, exempelvis `2.5.0-rc.1`, och dokumentera målgruppen/kanalen.

## Hotfix och rollback

Hotfix utgår normalt från aktuell `main` och använder `fix:` för en bakåtkompatibel korrigering.

Publicerade taggar ska inte flyttas eller skrivas om. Vid felaktig release:

1. återställ via vanlig PR om kodrollback behövs;
2. kör normal verifiering;
3. bumpa till en ny korrigerande version;
4. skapa ny tag/GitHub Release med tydlig relation till den felaktiga releasen.

Ingen force-push eller tag history rewrite används.

## Kvarvarande blocker

Full releaseautomation är ett separat arbete eftersom write-identitet/CI-triggerproblemet måste lösas utan nya onödiga credentials eller försvagade checks.
