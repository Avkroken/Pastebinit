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

Arbete sker i en **sluten pool av tre grenar**, en per arbetstyp:

| Slot | För |
| --- | --- |
| `work/feature` | ny funktionalitet |
| `work/fix` | buggfixar och CI-problem |
| `work/chore` | dokumentation, städning, konfiguration |

`main` tar bara emot squash-mergade PR:er som passerat gröna checkar.

**Skapa aldrig egna grenar.** Rulesetet blockerar det — en push som försöker
skapa något utanför poolen avvisas. Poolen finns för att grenar som skapas per
uppgift blir liggande halvfärdiga.

1. Välj sloten som matchar arbetet. Är den upptagen duger vilken ledig som helst —
   namnen är vägledning, inte en spärr. Ligger det omergat arbete i en slot,
   **slutför det först** i stället för att börja något nytt i en annan.
2. Kör relevanta tester och packaging-kontroller innan push.
3. Pusha till sloten och öppna PR från den till `main` som klar för granskning.
   Aktivera auto-merge — merge-kön tar PR:n så snart required checks är gröna.
4. Lös CI- och reviewproblem i samma slot; PR:n uppdateras av varje push.
5. **Squash merge är den enda tillåtna merge-metoden.** Efter merge rebasar
   `.github/workflows/sync-pool.yml` varje slot på `main`.

Skicka aldrig direkt till `main`, kringgå inte branch protection/rulesets och ändra
inte hemligheter eller organisationsinställningar utan uttrycklig instruktion.

## Svarsformat

**[SKILLS.md](SKILLS.md) styr allt svarsformat. Läs den och följ den i varje svar.**

SKILLS.md har företräde framför den här filen och framför varje annan
formuleringsanvisning i repot. Sammanfatta den inte, återge den inte i kortform
och väg den inte mot andra skrivelser — det är den filen som gäller.
