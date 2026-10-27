# Avvio in locale su Mac: prova con 10 contatti

Obiettivo: vedere le prime bozze vere di Harvey per Goodlearning, su pochi contatti, prima di costruire altro. Tempo: circa 30 minuti, più l'attesa delle bozze.

Serve: un Mac, un abbonamento Claude Pro o Max, e il CSV di Apollo. Nessuna chiave a pagamento e nessuna casella di invio: le email le copi e le mandi tu.

I comandi vanno scritti nell'app Terminale. Quelli con `#` davanti sono commenti, non vanno copiati.

## 1. Installazione

```bash
# Python 3.13: quello del Mac (3.9) è troppo vecchio per Harvey
brew install python@3.13 git

# Il repo, già sul ramo giusto
git clone -b claude/awesome-volta-5iw6pb https://github.com/evignocchi/goodlearning.git
cd goodlearning/harvey

# Ambiente di Harvey e dipendenze (3.13, non "python3")
python3.13 -m venv .venv && source .venv/bin/activate && pip install -e .
cp .env.example .env
```

Se `brew` non c'è, si installa da brew.sh. Ogni volta che apri un Terminale nuovo, rientra nella cartella `goodlearning/harvey` ed esegui `source .venv/bin/activate`.

## 2. Claude Code collegato al tuo abbonamento

Harvey scrive le email chiamando Claude Code, quindi deve essere installato e collegato.

```bash
claude --version        # se non c'è: installa Claude Code dal sito di Anthropic
claude login            # accedi con l'account dell'abbonamento Pro o Max
claude update           # Harvey vuole una versione recente
harvey status --check   # controlla che Claude sia utilizzabile da Harvey (non spende quota)
```

`harvey status --check` deve dire che la CLI è a posto. Se si lamenta della versione, rifai `claude update`.

## 3. Importa 10 contatti

Scegli 10 righe del CSV con ruoli diversi (qualche RSPP, qualche HR, qualche CEO). Il modo più semplice: copia il file, tieni la prima riga (le intestazioni) e cancella le altre righe che non vuoi.

```bash
harvey dashboard
```

Stampa un link con un token (`http://127.0.0.1:5555/#token=...`). Aprilo nel browser e tienilo privato. Poi:

1. Scheda **Contacts**, pulsante **Import list**, scegli il file di prova.
2. Leggi l'anteprima (righe, duplicati, nuovi contatti, senza email) e premi **Import**.
3. Lascia lo stato email su **Verified**.

Controlla che nella lista compaiano i 10 contatti.

## 4. Attiva i segnali

Da un altro Terminale (stessa cartella, con l'ambiente attivo):

```bash
harvey signals --confirm HIRING_ROLE,OPEN_ROLES,CERT_ISO,LMS_IN_USE
```

Sono i quattro che servono a Goodlearning: annunci di lavoro, certificazioni dichiarate e piattaforma di formazione già in uso. Gli altri restano spenti.

## 5. Fai scrivere le bozze

```bash
harvey run
```

Harvey ragiona a cicli. A ogni ciclo legge i siti delle aziende (segnali) e, se ci sono contatti da scrivere, prepara le email. Nel Terminale vedrai righe come `Decision: write_campaign` e `Writer: Campaign ... created`.

- La prima bozza può arrivare dopo qualche minuto: ogni email è una chiamata a Claude.
- **Fermalo con Ctrl+C appena le bozze sono pronte.** Dopo, Harvey passerebbe a cercare nuove aziende sul web, e per questa prova non serve.
- Se compaiono avvisi gialli sulla casella di invio o su Gmail, è normale: non ne abbiamo collegata una.

## 6. Leggi e copia le bozze

Nella dashboard, scheda **Outbox**: una bozza alla volta, con il contesto sotto (azienda, ruolo, segnali trovati, note del Writer).

- **Copy address**, **Copy subject**, **Copy text**: incolli nel tuo programma di posta.
- **Edit**: correggi il testo.
- **I sent it**: dopo che l'hai mandata, così Harvey non la riscrive.
- Non premere **Approve**: servirebbe a farle partire da Harvey, che non ha una casella.

Guarda anche **Signals** e **Companies**: dopo il primo ciclo dovresti vedere quali segnali sono stati trovati e dove.

## 7. Cosa mandarmi

Per ognuna delle 10 bozze, incolla qui:
- il ruolo e il settore (senza nome e cognome, se preferisci);
- il testo della bozza;
- i segnali che Harvey mostra per quell'azienda;
- se il tono, la lunghezza o l'apertura non ti convincono, una riga sul perché.

Con quelle correggo le regole di stile in italiano, il contesto e il piè di pagina.

## Uso di tutti i giorni: senza Terminale

Dopo la prima installazione non ti serve più scrivere comandi.

- **`Avvia Harvey.command`**: doppio clic. Si apre una finestra del Terminale (la lasci stare) e la dashboard compare nel browser. Da lì importi le liste (Contacts → Import list), scegli i segnali (Signals), avvii Harvey (Controls → Start Harvey) e leggi le bozze (Outbox). Per spegnere tutto chiudi la finestra: ferma anche Harvey.
- **`Aggiorna Harvey.command`**: doppio clic per scaricare le novità del progetto. Spegni Harvey prima.
- Per averlo sempre a portata di mano, trascina `Avvia Harvey.command` dal Finder sul Dock (a destra della linea, vicino al cestino) oppure sul Desktop tenendo premuto `Cmd + Opzione` per creare un alias.
- La prima volta macOS potrebbe chiedere conferma per aprire il file: scegli Apri. Se dice che non ha i permessi, scrivi una volta `chmod +x "Avvia Harvey.command" "Aggiorna Harvey.command"` dalla cartella `harvey`.
- Harvey lavora solo finché il Mac è acceso e la finestra è aperta.

## Se qualcosa non va

| Cosa vedi | Cosa fare |
|---|---|
| `command not found: harvey` | `source .venv/bin/activate` dalla cartella `goodlearning/harvey` |
| `ModuleNotFoundError: No module named 'harvey'` | Rilancia `harvey install`, poi riprova (Python 3.13 su Mac a volte ignora un file di collegamento) |
| `externally-managed-environment` | Stai usando il Python di sistema: rifai il passo 1 con `python3.13 -m venv .venv` |
| Harvey si ferma e dice di aggiornare Claude | `claude update` e rilancia |
| Nessuna bozza dopo 15-20 minuti | Guarda l'ultima riga del Terminale e mandamela. Controlla anche `harvey status` |
| La dashboard non si apre | Rilancia `harvey dashboard` e apri il link nuovo: il token cambia |

## Cosa tocca solo a te

- Il CSV con i nomi veri resta sul tuo Mac: non metterlo nel repo e non committarlo (la cartella `data/` è già esclusa da git).
- Le email che copi vanno inviate rispettando le regole sul contatto commerciale. Il piè di pagina che Harvey aggiunge oggi è in inglese e senza indirizzo postale: lo sistemiamo dopo questa prova, con il testo deciso da chi si occupa della privacy.
