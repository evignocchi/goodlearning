# Goodlearning: casi d'uso, formazioni obbligatorie e segnali di outreach

Uso interno di Harvey, non va citato nelle email. Obiettivo: collegare un obbligo o un problema reale a un evento osservabile, che è il vero motivo per scrivere oggi.

Principio: la certificazione in sé non è il segnale. Il segnale è l'evento che la rende urgente (scadenza, audit, assunzione, apertura di un cantiere, nuova normativa).

**Requisiti e durate non verificati.** Gli elenchi qui sotto sono una mappa di temi, non un riferimento legale. Durate, periodicità e validità (per esempio l'Accordo Stato-Regioni sulla formazione, rivisto di recente) vanno controllate da una persona prima di finire in un'email, in una risposta o in un contenuto commerciale. Nelle email si parla del tema ("scadenze della formazione", "prove per l'audit"), mai di ore, anni o articoli di legge.

## 1. Formazioni e certificazioni obbligatorie (temi)

**Sicurezza sul lavoro (D.Lgs. 81/08), la categoria più ricorrente**
- Formazione generale e specifica dei lavoratori e aggiornamento periodico
- Preposti, dirigenti, RLS, RSPP/ASPP
- Primo soccorso e antincendio
- Abilitazioni per attrezzature: carrelli elevatori, PLE, gru, escavatori, trattori
- Lavori in quota, DPI di terza categoria, spazi confinati
- Rischio elettrico (PES/PAV), movimentazione manuale dei carichi, videoterminali, rischio chimico, ATEX

**Protezione dati, compliance, responsabilità**
- GDPR (incaricati al trattamento), D.Lgs. 231/01 (modello organizzativo, ODV)
- Anticorruzione e whistleblowing, antiriciclaggio
- Cybersecurity: NIS2 impone formazione a organi direttivi e personale

**Settore specifico**
- Alimentare: HACCP, formazione igienica
- Sanitario: ECM, privacy sanitaria
- Finanza e assicurazioni: IVASS, MiFID, IDD
- Edilizia: patente a crediti, formazione specifica di cantiere
- Trasporti: CQC, ADR
- Manifatturiero e impiantistica: F-gas, saldatori (EN ISO 9606), PND, PES/PAV
- Formazione finanziata: Fondimpresa, Fondartigianato, Fon.Coop e altri fondi interprofessionali, con rendicontazione obbligatoria

**Certificazioni di sistema (la formazione serve per mantenerle)**
- ISO 9001, 14001, 45001, 27001, 37001, 22000
- IATF 16949 (automotive), AS9100 (aerospace)
- SA8000, parità di genere UNI/PdR 125

## 2. Casi d'uso, e quanto sono rilevabili da fuori

"Oggi" = Harvey può già captarlo con i segnali del catalogo; "da costruire" = serve un collector nuovo. Dalla versione con `CERT_ISO` e `LMS_IN_USE` sono "oggi" anche le certificazioni dichiarate e l'LMS già in uso.

| # | Caso d'uso | Problema reale | Rilevabile da fuori |
|---|---|---|---|
| 1 | Gestione scadenze formative | Excel con scadenze, nessuno sa chi è scoperto | Difficile; si deduce dal settore regolato |
| 2 | Onboarding rapido | Il nuovo assunto diventa operativo lentamente, il tutor perde tempo | Oggi: `HIRING_ROLE`, `OPEN_ROLES` (molte assunzioni) |
| 3 | Procedure su macchine pesanti / SOP | Know-how nella testa dei senior, errori e infortuni | Oggi: annunci per carrellista, gruista, operatore |
| 4 | Passaggio generazionale | Pensionamenti: il sapere esce dall'azienda | Da costruire (età di titolari, successori cercati) |
| 5 | Multi-sede / franchising | Stesso standard su molti punti | Da costruire (nuove sedi) |
| 6 | Formazione rete esterna | Agenti, installatori, rivenditori da formare sul prodotto | Da costruire (store locator, lanci) |
| 7 | Formazione commerciale | Nuovi prodotti, gestione obiezioni | Difficile |
| 8 | Audit readiness | Prove documentali per ISO, ispezioni, ASL | Oggi: `CERT_ISO` (dal sito; Accredia resta da costruire) |
| 9 | Lavoratori stranieri / multilingua | Formazione in più lingue con comprensione verificata | Difficile |
| 10 | Stagionali e turnover alto | Retail, ristorazione, logistica, turismo | Oggi: stesso annuncio ripubblicato (`OPEN_ROLES`) |
| 11 | Customer care e assistenza tecnica | Procedure e troubleshooting a portata di mano | Difficile |
| 12 | Compliance continuativa (GDPR, 231, NIS2) | Corsi annuali con tracciamento | Da costruire (settori NIS2) |
| 13 | Cambio software / ERP / processo | Adozione guidata del cambiamento | Difficile |
| 14 | Formazione fornitori e appaltatori | Responsabilità in solido su sicurezza e qualità | Difficile |
| 15 | Corsi vendibili ai clienti | Consulenti, associazioni, enti formativi che vendono formazione | Segmento a parte (enti di formazione) |

## 3. Dai casi d'uso ai segnali

Struttura: evento scatenante → segnale osservabile → fonte → decisore → messaggio.

| Caso d'uso | Segnale | Dove si capta |
|---|---|---|
| Onboarding | Molte assunzioni in poco tempo, annunci ripetuti per lo stesso ruolo | Job board, pagina "lavora con noi" |
| Turnover alto | Annuncio ripubblicato più volte | Job board, Glassdoor/Indeed |
| Macchine pesanti | Aziende con parco macchine (edilizia, logistica, agricoltura) che cercano carrellista, gruista, operatore | Annunci, SOA, albi |
| Audit / ISO | Annuncia o ottiene una certificazione ISO; annunci per responsabile qualità/HSE | Oggi: `CERT_ISO` dal sito. Registri Accredia e comunicati: da costruire |
| NIS2 | Settori nel perimetro NIS2, annunci per CISO/IT security | Elenchi settoriali, job board |
| Crescita / multi-sede | Nuove sedi o punti vendita, round di finanziamento | News, Google Maps, comunicati |
| Fondi formativi | Aderente a un fondo interprofessionale, bandi aperti | Bandi, siti dei fondi |
| Ricambio generazionale | Titolari o figure chiave oltre i 60; ricerca di successori tecnici | Registro imprese |
| Rete esterna | Rete di agenti o installatori, nuovo prodotto in lancio | Sito, comunicati |
| Formazione già in uso | LMS concorrente (link a piattaforme note, sottodomini elearning/lms/fad) | Oggi: `LMS_IN_USE` dal sito. Gli annunci che lo citano: da costruire |
| Cambio ruolo HR | Nuovo HR/Training manager da poco (finestra di acquisto) | Fonti fornite dall'utente |
| Infortuni e sanzioni | Sanzioni, incidenti, ispezioni | News locali, INAIL |

Su sanzioni e infortuni: non scriverne mai nell'email come fatto noto. Sono notizie su un'azienda, non un motivo gentile per contattare una persona, e un errore qui è molto più grave di un'email generica.

**Pesatura**
- Alto: l'azienda ha già il problema (scadenza vicina, audit annunciato, assunzioni di massa).
- Medio: contesto che lo rende probabile (settore regolato, crescita, nuovo HR).
- Basso: solo settore o dimensione. Senza un segnale alto o medio, la prima email resta un'osservazione onesta sul ruolo.

**Angolo del messaggio**
- Scadenza o obbligo: semplicità e controllo ("chi è scoperto" in un colpo d'occhio).
- Turnover o onboarding: tempo del tutor risparmiato, rapidità a diventare operativi.
- Audit: prove documentali pronte (tracciatura e report di GoodSuite).
- Rete esterna: standard uniforme, edizioni "esterne" e integrazione con le piattaforme dei clienti.

## 4. Priorità

I casi con obbligo + scadenza + segnale pubblico sono i più facili da trasformare in outreach: sicurezza (annunci HSE e per attrezzature), ISO, NIS2, turnover. Knowledge retention e onboarding sono più sentiti dai clienti ma più difficili da rilevare dall'esterno, quindi li usiamo come angolo della seconda email e non come motivo della prima.

Per il pilota: settore manifatturiero lombardo (è quello del primo elenco), con tre casi: audit/ISO e sicurezza, onboarding e turnover, ricambio generazionale. Segnali già disponibili: annunci (`HIRING_ROLE`, `OPEN_ROLES`), certificazioni dichiarate (`CERT_ISO`) e LMS già in uso (`LMS_IN_USE`). Da costruire: nuove sedi, ricambio generazionale, perimetro NIS2.
