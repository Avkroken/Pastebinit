# CI och branchflöde

`main` är den enda långlivade arbetsgrenen. Varje ändring görs på en kortlivad branch och går via PR till `main`. Auto-merge används inte; färdiga PR:er squash-mergas.

PR-CI körs på `pull_request`; efter-merge-verifiering körs på `main` där den behövs. Samma arbetscommit ska inte verifieras dubbelt i onödan.

Repot är i huvudsak Python. Den ordinarie Python-checken hålls enkel och stabil, medan release-/paketeringsjobb ligger separat. Required checks får inte filtreras bort på workflow-nivå om det kan lämna GitHub i `Expected/Pending`.

Dokumentation/processmetadata ska inte starta dyr paketering. Okänd kod/config ska däremot hellre köra mer CI än riskera att relevant verifiering hoppas över.
