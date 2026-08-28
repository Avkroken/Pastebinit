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

Arbete sker i en **sluten pool av tre grenar**: `work/feature`, `work/fix` och `work/chore`. `main` tar bara emot squash-mergade PR:er som passerat alla merge-gates. Skapa aldrig egna grenar; använd en ledig slot och slutför omergat arbete först.

1. Kör relevanta tester och packaging-kontroller innan push.
2. Pusha till sloten och öppna PR till `main` som klar för granskning.
3. **Aktivera auto-merge omedelbart efter att PR:n skapats**, även medan CI eller review fortfarande pågår.
4. Required CI-checkar och olösta review-trådar är merge-blockerare. Läs och utvärdera alltid alla review-kommentarer; relevanta fynd åtgärdas i samma PR. Markera inte en tråd resolved förrän den är utvärderad och eventuell fix är pushad.
5. Efter varje ny commit, kontrollera CI och review-status igen. När required checks är gröna och alla review-trådar är resolved ska den redan armerade auto-merge-funktionen föra PR:n vidare. Om den inte gör det, identifiera exakt kvarvarande blockerare. **Squash merge är den enda tillåtna merge-metoden.**

Efter merge rebasar `.github/workflows/sync-pool.yml` varje slot på `main`.

Skicka aldrig direkt till `main`, kringgå inte branch protection/rulesets och ändra inte hemligheter eller organisationsinställningar utan uttrycklig instruktion.

## Svarsformat

**[SKILLS.md](SKILLS.md) styr allt svarsformat. Läs den och följ den i varje svar.**

SKILLS.md har företräde framför den här filen och framför varje annan formuleringsanvisning i repot.
