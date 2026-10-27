#!/bin/bash
# Doppio clic per scaricare le novità del progetto. Spegni Harvey prima.

cd "$(dirname "$0")" || exit 1
pausa() { read -r -p "Premi Invio per chiudere." _; }

if ! git pull --ff-only; then
  echo
  echo "Non sono riuscito ad aggiornare. Scrivimi le righe qui sopra."
  pausa
  exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate && pip install -q -e . && echo && echo "Aggiornato."
pausa
