# CI och branchflöde

`main` är den enda långlivade arbetsgrenen. Varje ändring görs på en kortlivad branch och går via PR till `main`. **Squash merge är den enda tillåtna merge-metoden.** Head-branchen raderas automatiskt efter merge.

Auto-merge får aktiveras först när den aktuella PR-HEAD:en har verifierats: required checks ska vara gröna, relevanta review-trådar resolved och den aktiva policyn för `main` känd. Auto-merge används inte som ett test för om GitHub råkar blockera merge.

## Live merge-policy

Det aktiva rulesetet `Protect main` gäller default branch och har inga bypass actors. Det blockerar deletion och non-fast-forward/force push, kräver pull request och resolved review threads, använder 0 generella approvals och kräver inte last-push approval.

Required status checks är:

- `python`
- `scan-pr / osv-scan`

`strict_required_status_checks_policy` är `true`, vilket innebär att verifieringen måste gälla aktuell `main` och inte en äldre bas.

PR-CI körs på `pull_request`; efter-merge-verifiering körs på `main` där den behövs. Required contexts får inte filtreras bort på workflow-nivå på ett sätt som lämnar GitHub i `Expected/Pending`.

## Security

`scan-pr / osv-scan` är den required dependency-/sårbarhetscheck som faktiskt produceras för PR-HEAD. OSV Scanners återanvändbara PR-workflow använder `fail-on-vuln: true`, så en ny upptäckt sårbarhet gör jobbet rött.

CodeQL är inte konfigurerat som required status check eller Code Scanning merge-protection-regel i det verifierade rulesetet. Därför finns ingen CodeQL-threshold att dokumentera som aktiv merge-gate.

Trivy används inte som verifierad merge-gate i repositoryt och har därför ingen aktiv Trivy-threshold.

## Reviewtjänster

CodeRabbit är best effort och är inte required status check. Saknad, pending, rate-limited eller misslyckad CodeRabbit-status blockerar inte ensam merge. Faktiska relevanta findings ska däremot utvärderas och eventuella relevanta review-trådar måste vara resolved.

Copilot Code Review är rådgivande och inte required status check. Rulesetet har `review_on_push: true` och granskar inte draft-PR:er. Faktiska relevanta Copilot-findings ska hanteras som annan review-feedback.

Repot är i huvudsak Python. Den ordinarie Python-checken hålls enkel och stabil, medan release-/paketeringsjobb ligger separat. Dokumentation/processmetadata ska inte starta dyr paketering. Okänd kod/config ska däremot hellre köra mer verifiering än riskera att relevant kontroll hoppas över.
