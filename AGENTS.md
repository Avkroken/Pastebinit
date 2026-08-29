# AGENTS.md

Den här filen innehåller instruktioner för AI-agenter som arbetar i repositoryt. Live repository configuration är verkställande sanning: när dokumentation och faktisk GitHub-enforcement skiljer sig ska den tillämpliga live-regeln följas och mismatchen rapporteras.

Root-`AGENTS.md` är den auktoritativa källan för repositoryövergripande agentpolicy. En mer specifik `AGENTS.md` längre ned i katalogträdet får lägga till regler för sitt subtree, men ska inte duplicera eller motsäga den repositoryövergripande policyn.

Följ dessutom de repository-specifika instruktionerna längre ned i denna fil.

<!-- AVKROKEN-COMMON:START -->

## Arbetsprincip

Leverera fungerande, verifierade och avgränsade ändringar. CI, GitHub Copilot Code Review och mänskliga reviewers är oberoende verifieringslager och ska inte vara den första debuggern för fel som agenten rimligen kan upptäcka själv före en pull request. Ändra inte mer än uppgiften kräver och bevara befintlig arkitektur och repository-specifika konventioner. Inför inte breaking changes om de inte uttryckligen krävs av uppgiften.

## Innan implementation

1. Läs denna fil och eventuell närmare `AGENTS.md` för de filer som berörs.
2. Läs relevant implementation, tester, konfiguration och närliggande dokumentation innan lösningen bestäms.
3. Identifiera repositoryts faktiska build-, test-, lint-, typecheck- och CI-kommandon från befintlig konfiguration.
4. Följ repositoryts branchmodell. Skapa inte egna branchkonventioner och anta inte att en policy är ruleset-enforced utan att den faktiskt är det.
5. Gör minsta kompletta ändring som löser problemet.

## Pre-PR quality gate

Innan en ready pull request skapas eller uppdateras ska agenten granska hela den egna diffen mot PR:ns base branch, kontrollera korrekthet, säkerhet, felhantering, kompatibilitet och relevanta edge cases, köra relevanta tester samt tillämplig lint/typecheck/build, lägga till eller uppdatera tester när beteende ändras och detta är praktiskt testbart, kontrollera att inga secrets/credentials/debugrester/oavsiktliga filer lagts till och fixa legitima egna findings före extern review. Efter senare commits ska påverkad validering köras igen; om full validering inte är möjlig ska begränsningen dokumenteras konkret.

## Review-signal

Prioritera funktionell och teknisk signal framför redaktionell puts. Rapportera inte rena stavnings-, grammatik-, interpunktions-, wording- eller stilfel i mänskligt läsbar prosa. Rapportera däremot textfel som materiellt kan ändra teknisk betydelse, säkerhet, korrekthet, användarbeteende eller bokstavliga instruktioner samt typos i maskin- eller semantikbärande innehåll såsom identifierare, strängkonstanter, paths, config keys, environment-variabler, API-fält, kommandon, flags, selectors, protokoll- och enumvärden.

## Reviewnivå och eskalering

Använd lägsta reviewnivå som ger tillräcklig säkerhet. Low använder Copilot Lite; Medium använder Balanced; High använder minst Balanced och vid behov den installerade OpenAI Codex-agenten via det faktiska GitHub-handle som GitHub visar; Critical använder Balanced + Codex och vid kvarstående kritisk tvetydighet den installerade Anthropic Claude-agenten via dess faktiska GitHub-handle. Gissa eller hårdkoda inte mention-namn från andra workflows eller exempel. Bygg inte ett nytt router-workflow enbart för eskaleringen.

## Pull request och merge

Pusha aldrig direkt till `main`. Följ repositoryts branchmodell och skapa en ready PR först när pre-PR-gaten är genomförd.

Efter varje ny commit eller push ska aktuell HEAD, required checks/CI, mergeability och mergekonflikter verifieras igen. Läs och utvärdera dessutom alla review-kommentarer och alla nya, öppna eller återöppnade review-trådar; relevanta findings ska åtgärdas innan PR:n betraktas som klar.

När GitHub bedömer PR:n som direkt mergebar och alla tillämpliga live gates är uppfyllda — required checks/CI är godkända, inga mergekonflikter finns, inga relevanta obligatoriskt olösta review-trådar eller andra blockers återstår och ingen relevant review-feedback är outhanterad — ska PR:n mergas omedelbart.

Försök inte aktivera auto-merge på en PR som redan är direkt mergebar. Använd auto-merge när PR:n ännu inte kan mergas enbart därför att obligatoriska gates fortfarande väntar och repositoryt stöder auto-merge. Repositoryts live ruleset, merge queue och inställningar bestämmer tillåten merge-metod. Forcera eller kringgå inte repositoryskydd.

## Credentials och AI-infrastruktur

Committa eller exponera aldrig secrets, tokens, privata nycklar eller andra credentials. Lägg inte till externa AI-provider-credentials eller ändra billing/Copilot-policy/repository secrets/organisationsinställningar enbart för AI-routing utan uttryckligt ägargodkännande. Föredra befintliga GitHub/Copilot-native mekanismer.

## Verifiering efter ändringar

Ett lyckat API-svar, workflow-anrop eller deployment-request är inte i sig bevis på att ändringen är aktiv. När uppgiften ändrar GitHub-inställningar, permissions, deployments, routes, bindings eller annan runtime-/live-konfiguration ska relevant resulterande state verifieras efter ändringen.

## Definition of done

För en uppgift som skapar eller uppdaterar en pull request är arbetet inte klart förrän implementationen är färdig och avgränsad, relevanta tester/checks har körts eller begränsningen dokumenterats, diffen självgranskats, all review-feedback lästs och utvärderats, legitima findings åtgärdats, PR-status verifierats mot aktuell HEAD, eventuell live-state verifierats när tillämpligt och PR:n antingen mergats när alla gates är uppfyllda eller har auto-merge aktiverat när endast väntande obligatoriska gates återstår.

För read-only reviews, investigations, frågor eller live-konfigurationsuppgifter utan PR gäller inte PR-/mergekraven ovan; uppgiften är klar när efterfrågat arbete är genomfört och relevant resulterande status verifierats.

<!-- AVKROKEN-COMMON:END -->

## Repository-specifika instruktioner

### Branchmodell

Skapa en kortlivad arbetsgren för varje logisk ändring och öppna PR mot `main`. Kringgå aldrig branch protection, rulesets, required status checks, reviews, review-thread resolution, merge queues eller force-push restrictions.

### CI och validering

Använd repositoryts befintliga scripts och tooling. Inspektera `package.json`, taskfiler, scripts och dokumentation innan kommandon väljs. Required check-namn ska matcha GitHubs faktiska check contexts exakt. Ersätt inte repository-specifik CI med en generisk workflow enbart för governance och försvaga inte validering för att göra en PR mergebar.

### Säkerhet

Använd repositoryts etablerade secret-management- och environment-variable-mönster. Validera opålitlig extern input vid lämpliga boundaries och upprätthåll auth/authz server-side där det är relevant. Försvaga inte säkerhetskontroller för att få tester, builds eller deployments gröna.

### UI och design

För ändringar som berör UI, components, pages, styling eller layout ska `DESIGN.md` läsas först när filen finns. Återanvänd design tokens/components, bevara semantisk HTML och keyboard accessibility, säkerställ focus states/accessibility names, använd inte enbart färg för state och verifiera responsive behavior för berörda UI-flöden.

### Dependencies

Undvik nya dependencies när plattformen, ramverket eller en befintlig dependency redan löser behovet. Håll nödvändiga nya dependencies snävt avgränsade och motivera dem i PR:n.
