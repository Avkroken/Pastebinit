# Release- och versionsstandard

**Senast verifierad:** 2026-09-28

Det här dokumentet gäller **Pastebinit-repositoryt**. Repositoryts egna filer, taggar och workflows är source of truth för package-, release- och versionskontraktet.

## Versionskälla

Pastebinit använder SemVer-taggar i formen `vMAJOR.MINOR.PATCH` som canonical releaseversion.

`pyproject.toml` använder `setuptools-scm`, så package-versionen härleds från Git-historiken i stället för från ett separat manuellt versionsfält. Vid release bygger workflown wheel och sdist med exakt releaseversion och bifogar båda till GitHub Release.

Inför inte `version.txt` eller ett andra manuellt versionsankare.

## PR-titlar och merge queue

PR-titlar ska följa Conventional Commits:

```text
<type>[optional scope][!]: <description>
```

Tillåtna typer är `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `build`, `ci`, `chore` och `revert`.

`.github/workflows/pr-title.yml` validerar pull requests och rapporterar samma required-check-context för `merge_group`. Workflown använder inga secrets och har `permissions: {}`.

## SemVer

Automatisk versionsberäkning följer:

- breaking change -> **major**;
- `feat` -> **minor**;
- `fix`, `perf` och `revert` -> **patch**;
- `refactor`, `docs`, `test`, `build`, `ci` och `chore` skapar normalt ingen release ensamma;
- `Release-As: major|minor|patch|none` kan uttryckligen klassificera en icke-breaking ändring;
- en breaking change kan aldrig sänkas under major av `Release-As`.

## Automatiskt releaseflöde

`.github/workflows/release.yml` äger releaseprocessen lokalt i repositoryt:

```text
PR
  -> Conventional Commit-kompatibel PR-titel
  -> ordinarie Python-CI/review
  -> merge till main
  -> Python 3.10 och Python 3.14 verifierar samma main-SHA
  -> semantic release beräknar SemVer
  -> wheel + sdist byggs med releaseversionen
  -> immutable tagg
  -> GitHub Release med changelog + package-artefakter
```

Releasejobbet kör endast på `main`, använder full Git-historik, kräver checks i `.github/release-required-checks`, vägrar divergerande releasehistorik och publicerar inte om någon observerad check misslyckas.

Canonical tagg- och GitHub Release-publication behöver ingen PAT eller extern releasebot. Det valfrria rådgivande Copilot-jobbet använder separat read-only `COPILOT_GITHUB_TOKEN`.

## Package-publicering

GitHub Release bifogar wheel och sdist. Automatisk publicering till PyPI eller annan extern registry ingår **inte** utan ett separat credential- och distributionsbeslut.

## Changelog

GitHub Releases är canonical versionerad changelog. Release notes genereras från first-parent-historiken och grupperas efter Conventional Commit-typ. Breaking changes markeras tydligt utan att tappa sin grundkategori.

`debian/changelog` är separat packaginghistorik och ersätter inte repositoryts releasehistorik.

## Prerelease

Manuell `workflow_dispatch` kan skapa `vMAJOR.MINOR.PATCH-rc.N`. Promotion till stable använder den aktiva RC:ns commit och tar inte med senare `main`-commits implicit.

## Hotfix och rollback

Publicerade taggar flyttas inte. En korrigering går via vanlig PR, normal verifiering och en ny SemVer-release. Ingen force-push eller tag history rewrite används.

## Copilot-sammanfattning

Releaseflödet kör den SHA-pinnade `github/copilot-release-notes`-actionen i ett separat read-only-jobb med `contents: read` och `pull-requests: read`. Copilot CLI förinstalleras i exakt version `1.0.90` innan `COPILOT_GITHUB_TOKEN` exponeras, så actionen använder den redan installerade binären i stället för att hämta en flytande CLI-version.

`COPILOT_GITHUB_TOKEN` ska vara en least-privilege fine-grained PAT med `Copilot Requests: Read` och en tokenägare med aktiv Copilot-licens. Workflown skapar eller roterar ingen credential. Om secreten saknas eller Copilot-genereringen misslyckas påverkas inte releaseprocessen.

Copilot-resultatet publiceras endast i GitHub Actions run summary som rådgivande text. Det skrivs inte in i den kanoniska GitHub Release-body:n. SemVer, release-target, required checks och release notes i GitHub Release fortsätter därför att komma enbart från `semantic_release.py`; osäkra eller ofullständiga AI-resultat kan aldrig ändra canonical changelog.
