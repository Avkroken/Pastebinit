# Starter-workflow-analys för rulesets

## Aktuell repo-yta

Repositoryt är ett Python-projekt med `pyproject.toml`, tester under `tests/` och Debian-paketering under `debian/`.

## Valda standardmallar

- `actions/starter-workflows/ci/python-app.yml`, ifylld för `main` och Python 3.14. Installationssteget behåller standardmallens struktur men installerar repositoryt och dess `test`-extra så att mallens pytest-steg kör repositoryts faktiska tester.
- `actions/starter-workflows/code-scanning/dependency-review.yml`, ifylld för `main`.
- `actions/starter-workflows/.github/dependabot.yml`, med package ecosystem anpassat från exempelvärdet `npm` till repositoryts `pip`, plus GitHub Actions.

Action-referenserna är SHA-pinnade till motsvarande versionsreferenser från standardmallarna för att följa repositoryts Actions-policy utan att lägga till egen workflow-logik.

## Föregående observerade checks

Den senaste egna `CI`-körningen på `main` var grön. Jobbet hette `python`, körde Python 3.14.7, installerade `.[test]`, kompilerade källkod/tester och avslutade med 51 av 51 pytest-tester godkända.

GitHubs dynamiska CodeQL/default-setup-yta var också grön på samma `main`-commit. Därför läggs ingen lokal Advanced CodeQL-workflow till.

## Required checks

Rulesetet uppdateras inte förrän de nya standardmallarna faktiskt har producerat observerbara checknamn på denna PR-branch. Den tidigare required checken `python` ersätts därför inte genom antagande.

## Funktioner som standardmallarna inte täcker

Den tidigare CI:n hade ett separat `compileall`-steg. Python application-standardmallen har i stället sitt standardiserade flake8-steg före pytest. Inget eget compileall-steg läggs till utanför standardmallens ram.

Repositoryts Debian release-workflow, den organisationsspecifika Release Please-wrappern och tidigare OSV-workflow ersätts inte med egna workflows om ingen direkt motsvarande mall finns i `actions/starter-workflows`.

Security-alert-specifika issue- eller PR-mallar byggs inte lokalt om motsvarande GitHub-standardmall saknas i starter-workflows.
