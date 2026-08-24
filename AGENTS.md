# pastebinit — AI Agent Guide

Python-CLI för att skicka text och filer till pastebin-tjänster, med Python-packaging och Debian-paketering.

## Teknik och kommandon

- Python ≥ 3.10, setuptools/`pyproject.toml`, pytest.
- Installera utvecklingsmiljön med `pip install -e ".[dev]"` och kör tester med `pytest`.
- Debian-paket byggs med `dpkg-buildpackage -b -us -uc`; byggartefakter ska inte committas.
- Credentials ska hanteras via keyring eller motsvarande säker lagring, aldrig hårdkodas.

## Release

Release- och `.deb`-workflows ska hållas separerade från PR-CI. Manuella ombyggen av ett befintligt release-tag hanteras via workflow-dispatch när det stöds av repots workflow.

## GitHub-arbetsflöde

`main` är den enda långlivade arbetsgrenen. `dev` används inte.

1. Skapa en kortlivad branch från aktuell `main` för varje uppgift.
2. Kör relevanta tester och packaging-kontroller innan push.
3. Öppna PR från arbetsbranchen till `main` som klar för granskning. Auto-merge är tillåtet och får aktiveras när PR:n är redo; GitHub mergar först när alla ruleset-krav är uppfyllda.
4. Lös CI- och reviewproblem på samma branch tills required checks är gröna och review-trådar lösta.
5. **Squash merge är den enda tillåtna merge-metoden.** Använd inte merge commits eller rebase merge. Repot är konfigurerat att automatiskt radera head-branchen efter merge.

Skicka inte direkt till `main`, kringgå inte branch protection/rulesets och ändra inte hemligheter eller organisationsinställningar utan uttrycklig instruktion.

## Svarsformat

Led med nästa åtgärd eller resultat. Numrera flerstegsarbete, håll listor korta och ange konkret orsak/fix vid fel.
