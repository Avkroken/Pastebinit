# AGENTS.md

Den här filen är den auktoritativa repositoryövergripande arbetsinstruktionen. En närmare `AGENTS.md` får lägga till regler för sitt subtree men får inte motsäga reglerna här.

## Repository

`pastebinit` är ett Python-projekt med testsvit under `tests/` och Debian-paketering under `debian/`. Den manuella `.deb`-releaseworkflowen är separat från PR-CI.

Credentials, tokens och andra secrets får aldrig hårdkodas eller committas.

## Brancher och pull requests

- Pusha aldrig direkt till `main`.
- Arbeta på en kortlivad branch och öppna en ready pull request till `main`.
- Auto-merge får aktiveras först när aktuell PR-HEAD har passerat samtliga required checks, relevanta review-trådar är resolved och den aktiva policyn för `main` är verifierad.
- Använd inte direkt merge om det inte uttryckligen har begärts.
- Repositoryts live-ruleset tillåter endast squash merge till `main`.
- Repositoryt använder inte merge queue och har ingen obligatorisk återanvändbar branchpool.

## Merge-gates

Live-konfigurationen är sanningskällan. För `main` gäller rulesetet `Protect main`:

- required status checks: `python` och `scan-pr / osv-scan`
- `strict_required_status_checks_policy: true`, så PR:n måste verifieras mot aktuell `main`
- pull request krävs före merge
- required approvals: 0
- last-push approval krävs inte
- olösta review-trådar blockerar merge
- deletion och non-fast-forward/force push är blockerade
- Copilot Code Review använder `review_on_push: true`; drafts undantas
- endast squash merge är tillåtet
- inga bypass actors är konfigurerade

`scan-pr / osv-scan` är repositoryts dependency-/sårbarhetsgate för PR:er och failar när OSV Scanner rapporterar en ny sårbarhet. CodeQL och Trivy är inte konfigurerade som merge-gates i det verifierade rulesetet och ska inte antas vara obligatoriska utan ny live-verifiering.

CodeRabbit är best effort och är inte en required status check. Saknad, pending, rate-limited eller misslyckad CodeRabbit-status blockerar inte ensam merge. Om CodeRabbit faktiskt lämnar relevanta findings ska de verifieras och åtgärdas; relevanta review-trådar måste vara resolved innan merge.

Copilot Code Review är rådgivande och inte en required status check. Faktiska relevanta Copilot-findings ska ändå utvärderas och hanteras som annan review-feedback.

Alla review-kommentarer och review-trådar ska läsas och utvärderas. Relevanta findings åtgärdas i samma PR och en tråd markeras resolved först när eventuell nödvändig fix är pushad och verifierad.

Efter varje ny commit ska aktuell HEAD läsas tillbaka, required CI/security köras igen och review-status kontrolleras på nytt. Auto-merge får först därefter aktiveras när samtliga merge-gates för den aktuella HEAD:en är verifierade.

Om merge inte kan ske ska den konkreta blockeraren i live-ruleset, CI, security- eller review-state identifieras och rapporteras. Kringgå aldrig skyddet.

## Verifiering

- Läs relevant kod, `pyproject.toml`, tester och paketeringsfiler före ändringar.
- Granska hela diffen mot `main` före PR.
- Kör relevant pytest, compile/build och andra kontroller som ändringen påverkar.
- Testa Debian-paketering när `debian/` eller releaseflödet ändras.
- Lägg till eller uppdatera tester när beteende ändras och det är praktiskt testbart.
- Kontrollera att diffen inte innehåller secrets, debugrester eller oavsiktliga genererade filer.

## GitHub Actions

- `.github/workflows/ci.yml` producerar required context `python`.
- `.github/workflows/osv-scanner.yml` producerar required PR-context `scan-pr / osv-scan`.
- `.github/workflows/release-deb.yml` är ett manuellt releasejobb för en redan existerande tagg och ska inte blandas in i PR-CI.
- `.github/workflows/codex-issue-remediation.yml` skapar en körningsunik tillfällig branch under `automation/codex-issue/` och öppnar en PR, men armerar inte auto-merge innan aktuell HEAD är verifierad. Dessa branches undantas från PR-watchdog; repots `delete_branch_on_merge` tar bort dem efter merge.
- `.github/workflows/pr-watchdog.yml` kan öppna en PR för en lokal branch med unika commits som saknat PR för länge, men aktiverar inte auto-merge. State ligger på `automation/pr-watchdog-state`.
- `.github/workflows/auto-fix-review.yml` får begära en Codex-fix för uttryckligen betrodd review-feedback men får inte lösa review-tråden åt implementationen.

GitHub Actions ska pinnas till commit-SHA när praktiskt möjligt.

## Definition of done

En PR-baserad uppgift är klar först när implementationen är färdig, relevanta tester har körts eller en konkret begränsning dokumenterats, den slutliga diffen har granskats, all review-feedback har utvärderats, required `python` och `scan-pr / osv-scan` är gröna för exakt final HEAD, PR:n är verifierad mot aktuell `main`, relevanta review-trådar är resolved och merge har skett via tillåten squash-policy eller väntar på en verifierad legitim external gate.
