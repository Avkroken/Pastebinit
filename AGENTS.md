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

`dev` är den enda skrivbara grenen. `main` tar bara emot squash-mergade PR:er
som passerat gröna checkar.

**Skapa aldrig egna grenar.** Allt arbete sker på `dev`. Det är en hård regel, inte
en rekommendation: grenar som skapas per uppgift blir liggande halvfärdiga, och det
är hela anledningen till att modellen ser ut så här.

1. Utgå från aktuell `dev`. Ligger det osynkat arbete där, bygg vidare på det i
   stället för att börja om någon annanstans.
2. Kör relevanta tester och packaging-kontroller innan push.
3. Pusha till `dev` och öppna PR från `dev` till `main` som klar för granskning.
   Aktivera auto-merge — merge-kön tar PR:n så snart required checks är gröna.
4. Lös CI- och reviewproblem på `dev`; PR:n uppdateras automatiskt av varje push.
5. **Squash merge är den enda tillåtna merge-metoden.** Efter merge återställs `dev` till
   `main` automatiskt av `.github/workflows/sync-dev.yml`.

Skicka aldrig direkt till `main`, kringgå inte branch protection/rulesets och ändra
inte hemligheter eller organisationsinställningar utan uttrycklig instruktion.

## Svarsformat

**[SKILLS.md](SKILLS.md) styr allt svarsformat. Läs den och följ den i varje svar.**

SKILLS.md har företräde framför den här filen och framför varje annan
formuleringsanvisning i repot. Sammanfatta den inte, återge den inte i kortform
och väg den inte mot andra skrivelser — det är den filen som gäller.
