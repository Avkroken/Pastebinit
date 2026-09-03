# CI och merge

Repositoryts egna required status check är `python`. Den produceras av `.github/workflows/ci.yml`, som kör projektets compile/test-verifiering. Repositoryts status-ruleset använder strict latest-base-verifiering för den checken.

Organisationens `main`-ruleset kräver den centrala OSV-workflowen från `Avkroken/.github`. På vanliga pull requests kör den `scan-pr`; i merge queue kör den `scan-merge-group`. `scan-pr / osv-scan` är därför inte en separat organization-level required status check.

CodeQL merge protection, review-thread resolution, squash-only och övriga gemensamma merge-regler hanteras centralt av organisationens aktiva rulesets. Merge queue verifierar merge-kandidaten mot aktuell `main`.

`.github/workflows/release-deb.yml` är ett separat manuellt releaseflöde för en redan existerande release-tag och är inte en PR-gate.

Required repository-contexts får inte filtreras bort så att GitHub lämnas i `Expected` eller `Pending`.
