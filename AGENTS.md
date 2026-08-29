# AGENTS.md

Den här filen är den auktoritativa repositoryövergripande arbetsinstruktionen. En närmare `AGENTS.md` får lägga till regler för sitt subtree men får inte motsäga reglerna här.

## Repository

`pastebinit` är ett Python-projekt med testsvit under `tests/` och Debian-paketering under `debian/`. Den manuella `.deb`-releaseworkflowen är separat från PR-CI.

Credentials, tokens och andra secrets får aldrig hårdkodas eller committas.

## Brancher och pull requests

- Pusha aldrig direkt till `main`.
- Arbeta på en kortlivad branch och öppna en ready pull request till `main`.
- **Aktivera auto-merge omedelbart när PR:n skapats**, även medan CI eller review fortfarande pågår.
- Använd inte direkt merge om det inte uttryckligen har begärts.
- Repositoryts live-ruleset tillåter för närvarande endast squash merge.
- Repositoryt använder inte merge queue och har ingen obligatorisk återanvändbar branchpool.

## Merge-gates

Live-konfigurationen är sanningskällan. För `main` gäller för närvarande:

- required status check: `python`
- olösta review-trådar blockerar merge
- Copilot Code Review körs vid push till PR-grenen
- squash är enda tillåtna merge-metod

Alla review-kommentarer och review-trådar ska läsas och utvärderas. Relevanta findings åtgärdas i samma PR och en tråd markeras resolved först när eventuell nödvändig fix är pushad och verifierad.

Efter varje ny commit ska relevanta tester/CI köras igen och review-status kontrolleras på nytt. När required check är grön och alla relevanta review-trådar är resolved ska den redan armerade auto-merge-funktionen föra PR:n till `main`.

Om auto-merge inte sker ska den konkreta blockeraren i live-ruleset, review-state eller repositoryinställning identifieras och rapporteras. Kringgå aldrig skyddet.

## Verifiering

- Läs relevant kod, `pyproject.toml`, tester och paketeringsfiler före ändringar.
- Granska hela diffen mot `main` före PR.
- Kör relevant pytest, compile/build och andra kontroller som ändringen påverkar.
- Testa Debian-paketering när `debian/` eller releaseflödet ändras.
- Lägg till eller uppdatera tester när beteende ändras och det är praktiskt testbart.
- Kontrollera att diffen inte innehåller secrets, debugrester eller oavsiktliga genererade filer.

## GitHub Actions

- `.github/workflows/ci.yml` producerar required context `python`.
- `.github/workflows/osv-scanner.yml` är kompletterande dependency-/sårbarhetsverifiering och är inte required context i nuvarande ruleset.
- `.github/workflows/release-deb.yml` är ett manuellt releasejobb för en redan existerande tagg och ska inte blandas in i PR-CI.
- `.github/workflows/codex-issue-remediation.yml` skapar en körningsunik tillfällig branch under `automation/codex-issue/` och armerar auto-merge direkt. Dessa branches undantas från PR-watchdog; repots `delete_branch_on_merge` tar bort dem efter merge.
- `.github/workflows/pr-watchdog.yml` kan öppna en PR för en lokal branch med unika commits som saknat PR för länge och armerar auto-merge direkt. State ligger på `automation/pr-watchdog-state`.
- `.github/workflows/auto-fix-review.yml` får begära en Codex-fix för uttryckligen betrodd review-feedback men får inte lösa review-tråden åt implementationen.

GitHub Actions ska pinnas till commit-SHA när praktiskt möjligt.

## Definition of done

En PR-baserad uppgift är klar först när implementationen är färdig, relevanta tester har körts eller en konkret begränsning dokumenterats, den slutliga diffen har granskats, all review-feedback har utvärderats, required `python` är grön, relevanta review-trådar är resolved och auto-merge antingen har mergat PR:n eller är armerad medan en verifierad extern gate fortfarande väntar.
