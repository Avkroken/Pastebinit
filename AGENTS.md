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

## Merge-gates

Live-konfigurationen är sanningskällan. För `main` gäller organisationsrulesets med följande relevanta gates:

- required status checks: `python` och `scan-pr / osv-scan`
- strict latest-base-verifiering
- required approvals: 0; last-push approval krävs inte
- olösta review-trådar blockerar merge
- deletion och non-fast-forward/force push är blockerade
- Copilot Code Review är rådgivande, inte en required status check
- endast squash merge är tillåtet
- inga bypass actors är konfigurerade

CodeRabbit är best effort och inte en required status check. Faktiska relevanta findings från CodeRabbit eller Copilot ska ändå verifieras och åtgärdas. En review-tråd markeras resolved först när eventuell nödvändig fix är pushad och verifierad.

Efter varje ny commit ska aktuell HEAD, required CI/security och review-status kontrolleras på nytt. Kringgå aldrig repositoryts skydd.

## Verifiering

- Läs relevant kod, `pyproject.toml`, tester och paketeringsfiler före ändringar.
- Granska hela diffen mot `main` före PR.
- Kör relevant pytest, compile/build och andra kontroller som ändringen påverkar.
- Testa Debian-paketering när `debian/` eller releaseflödet ändras.
- Lägg till eller uppdatera tester när beteende ändras och det är praktiskt testbart.
- Kontrollera att diffen inte innehåller secrets, debugrester eller oavsiktliga genererade filer.

Om full lokal validering inte är möjlig ska begränsningen beskrivas konkret i PR:n.

## GitHub Actions

- `.github/workflows/ci.yml` producerar required context `python` och kör repositoryts Python-verifiering.
- `.github/workflows/osv-scanner.yml` är repositoryts egen OSV-definition och producerar required PR-context `scan-pr / osv-scan`.
- `.github/workflows/release-deb.yml` är ett manuellt releasejobb för en redan existerande tagg och ska inte blandas in i PR-CI.
- Repositoryts workflows får inte skapa eller uppdatera pull requests eller branches, arma eller genomföra merge, automatisera review, delegera remediation/kodarbete till AI-agenter eller lagra säkerhetsalert-snapshots. De centrala metadata-callers som beskrivs nedan är det enda metadata-only-undantaget och får inte ändra branch, review eller merge-state.
- Security alerts hanteras av GitHubs native säkerhetsfunktioner och kodändringar går genom repositoryts normala PR-gates.
- GitHub Actions ska pinnas till full commit-SHA.

## Metadata-only AI triage exception

Repositoryägaren har uttryckligen godkänt metadata-only issue triage via GitHub Agentic Workflows. Detta är ett smalt undantag från bredare förbud mot AI-delegering och gäller inte kodarbete eller remediation.

- `.github/workflows/metadata-routing.yml` får endast anropa Avkrokens centrala deterministiska metadata-routing för assignee och labels.
- `.github/workflows/issue-classification.yml` får endast trigga på öppnade/återöppnade issues, anropa den SHA-pinnade centrala `issue-classification.lock.yml` och efter lyckad klassificering anropa den SHA-pinnade centrala metadata-routingen.
- AI-delen får läsa det triggande issuet och read-only repositorykontext som behövs för klassificering.
- `gh-aw` safe outputs får endast lägga till exakt en temporär `classification:<difficulty>:<security>`-label från den centrala allowlisten. Den deterministiska routingen konverterar den till kanoniska `difficulty:*` och `security:*` labels och tar bort temporärlabeln.
- Befintliga kanoniska klassificeringslabels tar företräde över AI-output. Malformed eller konfliktande klassificeringsmetadata ska faila stängt till `triage:invalid`.
- Caller-workflowen får endast mappa `COPILOT_GITHUB_TOKEN` explicit till AI-workflowen; `secrets: inherit` är inte tillåtet.
- Workflowen får inte kommentera, assigna coding agents, skapa/ändra branches eller PR:er, reviewa, mergea, deploya eller utföra/föreslå remediation.
- Copilot-auth får komma från organization billing eller GitHub Actions-secreten `COPILOT_GITHUB_TOKEN`. Credentialvärden får aldrig committas, loggas eller kopieras till dokumentation.

Detta undantag ändrar inte säkerhets-, CI-, review- eller mergepolicyn.

## Definition of done

En PR-baserad uppgift är klar först när implementationen är färdig, relevanta tester har körts eller en konkret begränsning dokumenterats, den slutliga diffen har granskats, all review-feedback har utvärderats, required `python` och `scan-pr / osv-scan` är gröna för exakt final HEAD, PR:n är verifierad mot aktuell `main`, relevanta review-trådar är resolved och merge har skett via tillåten squash-policy eller väntar på en verifierad legitim external gate.

## PR-scope efter öppning

- När en PR har öppnats är dess avsedda scope fryst. Fortsatta commits får endast slutföra eller korrigera det scopet.
- Fel som orsakas av PR:ns befintliga ändringar ska rättas på samma branch/PR.
- Ny funktionalitet, opportunistiska refactors eller separata förbättringar ska få en ny branch och PR från aktuell `main`.
- Försök inte hinna lägga commits före eller under en pågående CI-/reviewkörning av tidsskäl.
- Efter varje korrigerande commit ska relevanta tester samt gate- och review-state verifieras på den nya HEAD:en.
