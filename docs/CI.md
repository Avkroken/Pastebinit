# CI och branchflöde

`main` är den enda långlivade arbetsgrenen. Varje ändring görs på en kortlivad branch och går via PR till `main`. **Squash merge är den enda tillåtna merge-metoden.**

Auto-merge får aktiveras först när den aktuella PR-HEAD:en har verifierats enligt repositoryts instruktioner. Om HEAD ändras ska checks, Code Scanning och review-state verifieras igen.

## Live merge-policy

Organisationens aktiva rulesets är verkställande sanning. Vid senaste live-verifieringen gäller för default branch:

- pull request krävs;
- 1 approval krävs;
- stale approvals avfärdas efter push;
- senaste pushen måste godkännas av någon annan än den som gjorde den;
- review-trådar måste vara resolved;
- deletion och non-fast-forward/force push blockeras;
- inga bypass actors är konfigurerade;
- endast squash merge är tillåtet.

Required status checks är:

- `python`
- `scan-pr / osv-scan`

`strict_required_status_checks_policy` är `true`, vilket innebär att verifieringen måste gälla aktuell `main` och inte en äldre bas.

Org-rulesetet `main` använder dessutom CodeQL Code Scanning merge protection med `medium_or_higher` för security alerts och `errors_and_warnings` för övriga alerts. Samma org-ruleset refererar för närvarande till Regelverkets `.github/workflows/osv-scanner.yml` som central required workflow; det är organisationsnivå och måste ändras separat om den centrala OSV-kopplingen ska tas bort.

## Repository-CI

`.github/workflows/ci.yml` producerar `python` och kör projektets compile/test-verifiering.

`.github/workflows/osv-scanner.yml` är repositoryts egen OSV-definition. PR-jobbet producerar `scan-pr / osv-scan`; scanning på `main`, schema och manual används för kompletterande rapportering.

`.github/workflows/release-deb.yml` är ett separat manuellt releaseflöde för en redan existerande release-tag och är inte en PR-gate.

Required contexts får inte filtreras bort på workflow-nivå så att GitHub lämnas i `Expected`/`Pending`.

## Reviewtjänster

CodeRabbit och Copilot Code Review är rådgivande och inte required status checks. Otillgänglighet, quota eller rate limit blockerar inte ensam merge. Faktiska relevanta findings ska däremot utvärderas och relevanta review-trådar måste vara resolved före merge.
