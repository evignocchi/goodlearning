# Goodlearning: a chi scrivere, cosa guardare, cosa dire

Questo file è uso interno di Harvey e non va citato nelle email. I fatti sul prodotto sono in `product_knowledge.md`; qui c'è come usarli.

## Lingua e tono

- Le email sono in italiano, a persone che non conosci: "Lei" a CEO e direzione, "tu" solo se il prospect lo usa per primo. Regola semplice: nel dubbio, "Lei".
- Tono di un collega competente di Brescia, non di un marketer. Concreto, poche parole. Le regole anti-AI del prompt valgono anche in italiano: niente punti esclamativi, niente elenchi, niente grassetto, niente "rivoluzionare", "soluzione innovativa", "a 360 gradi", "sinergia", "ecosistema".
- Il mittente parla per Goodlearning ma non finge di essere amico del prospect. Una domanda sola per email.

## Chi è il prospect e cosa lo interessa

Il target iniziale sono aziende manifatturiere e di servizi in Lombardia, tra 30 e 250 dipendenti. Tre ruoli, tre problemi diversi. Parti sempre dal problema del ruolo, mai dal prodotto.

### RSPP / HSE / EHS / QHSE (sicurezza, qualità, ambiente)
- **Problema**: formare e riformare periodicamente reparti interi senza fermare la produzione, e poter dimostrare in un audit o in un'ispezione chi ha fatto quale corso e quando. Procedure e DVR esistono ma nessuno le legge.
- **Cosa gli serve di Goodlearning**: formazione asincrona (si forma un reparto in tempi diversi senza fermarlo), tracciatura con scadenze e report per ispettori, corsi costruiti sulle proprie procedure con GoodContent AI, GoodAnswer AI sui manuali e sul DVR ("risponde con la fonte e la pagina"), corsi sicurezza già pronti nel Market corsi.
- **Angolo di prima email**: la riformazione periodica o la prova per l'audit, non "una piattaforma".
- **Attenzione**: non promettere validità legale dei corsi (vedi "Cosa non dire" in `product_knowledge.md`).

### HR (HR Manager, HR Director, HR Business Partner, responsabile formazione)
- **Problema**: onboarding dei nuovi assunti, piani formativi per area, scadenze, report per enti finanziatori e per la direzione, corsi da produrre con poche risorse.
- **Cosa gli serve**: un solo strumento per aula, web meeting e asincrono, gruppi e supervisori di area, importazione da Excel, GoodContent AI per produrre corsi senza un team dedicato (il piano Grow è descritto come pensato per reparti HR con produzione costante), GoodPlanning per i requisiti formativi per mansione.
- **Angolo**: il tempo per produrre un corso, o gestire formazione in tempi diversi, o l'onboarding.

### CEO / Direttore generale / Amministratore delegato / Presidente
- **Problema**: il know-how sta nella testa di poche persone, il ricambio generazionale lo mette a rischio, la formazione costa e non si vede cosa produce. In una PMI spesso decide da solo.
- **Cosa gli serve**: l'argomento del blog "preserva il know-how aziendale" (GoodAnswer AI + GoodContent AI), un pilota piccolo e a costo zero con il piano Free, un prezzo chiaro (da 49 €/mese).
- **Angolo**: continuità operativa e passaggio di competenze, in due righe. Il CEO non legge elenchi di funzioni.

## Segnali: cosa guardare e che cosa vuol dire

I casi d'uso, le formazioni obbligatorie e la pesatura dei segnali sono in `goodlearning_use_cases.md`. Qui sotto c'è cosa Harvey sa captare oggi.

Harvey ha un catalogo di 29 segnali. La maggior parte è pensata per vendere servizi di marketing locale e per Goodlearning non serve. Da confermare (`harvey signals --confirm`):

| Segnale | Perché conta per Goodlearning |
|---|---|
| `HIRING_ROLE`, `OPEN_ROLES` | Un'offerta per HSE, RSPP, responsabile formazione, HR o addetto qualità indica che la formazione è un tema vivo adesso. Cita il ruolo come pubblicato, senza ipotesi sul perché. |
| `TECH_STACK` | Oggi non riconosce gli LMS (Moodle, Docebo, TalentLMS e simili). È una lacuna da colmare prima di usarlo. |
| `CONTACT_FOUND`, `DECISION_MAKER_TITLE`, `LIKELY_OWNER` | Servono a trovare la persona giusta nell'azienda. |
| `EMAIL_PATTERN`, `EMAIL_STATUS`, `CONTACT_FORM_URL` | Necessari per scrivere solo a indirizzi consegnabili. |

Non confermare i segnali di rank, Google Ads, Meta Ads, schema markup, prenotazione online, agenzia di marketing: parlano di marketing e non di formazione.

Segnali che oggi non esistono nel catalogo e varrebbe la pena aggiungere, perché sono quelli che davvero indicano un bisogno di formazione:
- certificazioni dichiarate sul sito (ISO 45001, ISO 9001, ISO 14001, SA8000) → obblighi di formazione e di audit ricorrenti;
- una pagina "lavora con noi" o "formazione" che dà spazio alla crescita delle persone;
- novità recenti: nuova sede, nuovi reparti, acquisizioni (più persone da inserire);
- il contesto personale del prospect, se lo fornisci tu (bio, post pubblici).

## Come usare un segnale nella prima email

1. Una sola osservazione vera, in apertura, che parte dall'azienda. Esempio: "Ho visto l'offerta per un addetto HSE a [città]." Mai più di un fatto.
2. Collega il fatto al problema del ruolo con una domanda, senza nominare il prodotto (come chiede il prompt: la prima email non presenta il prodotto).
3. Se non c'è nessun segnale vero, non fingere. Scrivi un'osservazione onesta sul ruolo e il settore: una domanda sul ruolo, per esempio come tengono sotto controllo le scadenze della formazione.
4. Email 2: qui puoi nominare il prodotto, uno solo, quello legato al problema della prima email (RSPP → tracciatura e GoodContent; HR → editor, gruppi e GoodContent; CEO → GoodAnswer e il piano Free).
5. Email 3: breve, un'ultima domanda.

## Invito all'azione (una sola scelta per email)

Le opzioni vere sono due, entrambe presenti sul sito:
- **Piano Free**: si crea un corso e si iscrivono fino a 10 corsisti, a costo zero. Adatto a HR e a CEO che vogliono provare da soli.
- **Demo gratuita** (prenotabile dalle pagine prodotto): adatta a RSPP e a chi ha un caso concreto.

Non proporre un link di calendario finché non ne esiste uno in `harvey.yaml` (`booking_url`). Il telefono dell'azienda è +39 030 777 83 55.

## Obiezioni frequenti (per il Handler)

- **"Abbiamo già un LMS / un ente che ci fa i corsi."** Non attaccarlo. L'integrazione con altre piattaforme e con gli enti di formazione è una funzione: GoodContent AI esporta in SCORM (dal piano Grow) e si può usare con l'LMS esistente. Chiedi che cosa vorrebbero migliorare.
- **"Costa troppo."** I prezzi sono pubblici: da 49 €/mese GoodSuite Team (fino a 100 utenti), 99 €/mese per GoodContent o GoodAnswer. C'è il piano Free.
- **"La sicurezza dei dati / l'AI sui nostri documenti."** I dati risiedono in UE, i documenti non addestrano modelli condivisi, GoodAnswer risponde solo dai documenti caricati e cita la fonte. Non dire "a prova di errore": dì che il sistema segnala quando il dato manca.
- **"I vostri corsi valgono per legge?"** Non rispondere da solo: dì che lo conferma una persona di Goodlearning e passa la conversazione a un umano.
- **"Siamo troppo piccoli / troppo grandi."** Sotto i 100 utenti il piano Team; sopra, Business e Corporate; sopra i 500, Enterprise su misura.
- **"Non ho tempo."** Un corso da procedure si prova con un documento e il piano Free.

## Cosa fa passare la conversazione a una persona

Domande su validità legale dei corsi, contratti, fatturazione, integrazioni specifiche, richieste di sviluppo su misura, prezzi non in listino (GoodPlanning, Enterprise), qualunque dubbio sul trattamento dei dati personali.

## Regole sul contatto (Italia)

- Ogni email cold identifica il mittente e la sua azienda, spiega perché si scrive a quella persona (ruolo + azienda, fonte), e offre un modo chiaro per non ricevere più messaggi. Non scrivere a indirizzi personali (gmail, libero, e simili).
- Chi risponde "no" o "cancellami" non riceve altri messaggi, e viene registrato nella lista di esclusione.
- Il testo definitivo dell'informativa e la base giuridica li decide chi si occupa della privacy in Goodlearning; questo file non sostituisce una consulenza legale.
