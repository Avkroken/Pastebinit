# CI och branchflöde

Repositoryt använder endast `dev` och `main`. Arbete görs på `dev`, PR går `dev → main`, och efter merge fast-forwardar `.github/workflows/sync-dev.yml` automatiskt `dev` till `main` utan force-push. Om `dev` innehåller omergat arbete ska synken avbryta.

Vanlig CI ska inte köras dubbelt som både `push` till `dev` och `pull_request` för samma commit. PR-CI körs på PR; verifiering efter merge körs på `main`.

Repot är i huvudsak Python och har därför liten nytta av en separat språk-router. Den befintliga Python-checken behålls enkel och stabil. Separata release-/paketeringsjobb får filfilter när påverkan kan avgöras säkert. Required checks får inte filtreras bort på workflow-nivå om det kan lämna GitHub i `Expected/Pending`.

Dokumentation/processmetadata ska inte starta dyr paketering. Okänd kod/config ska däremot hellre köra mer CI än riskera att relevant verifiering hoppas över.