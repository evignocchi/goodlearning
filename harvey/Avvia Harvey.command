#!/bin/bash
# Doppio clic per avviare Harvey. Si apre la dashboard nel browser.
# Per spegnere tutto (anche Harvey, se lo hai avviato) chiudi questa finestra
# oppure premi Ctrl+C.

cd "$(dirname "$0")" || exit 1

pausa() { read -r -p "Premi Invio per chiudere." _; }

if [ ! -f .venv/bin/activate ]; then
  echo "L'ambiente di Harvey non c'è ancora. Segui prima i passi 1-8 di AVVIO_LOCALE.md."
  pausa
  exit 1
fi
# shellcheck disable=SC1091
source .venv/bin/activate

PORT=5555

# Già acceso? Riapro solo il browser.
if curl -s -o /dev/null "http://127.0.0.1:$PORT/"; then
  echo "La dashboard è già accesa: la riapro nel browser."
  open "$(harvey dashboard --url)"
  sleep 2
  exit 0
fi

harvey dashboard > /dev/null 2>&1 &
DASH=$!

spegni() {
  trap - EXIT
  # Harvey avviato dalla dashboard resta vivo da solo: lo fermo con la dashboard.
  if [ -f data/harvey.pid ]; then
    PID=$(cat data/harvey.pid 2>/dev/null)
    if [ -n "$PID" ] && ps -p "$PID" -o command= 2>/dev/null | grep -q harvey; then
      kill "$PID" 2>/dev/null
    fi
  fi
  kill "$DASH" 2>/dev/null
}
trap 'exit 0' HUP INT TERM
trap spegni EXIT

for _ in $(seq 1 30); do
  curl -s -o /dev/null "http://127.0.0.1:$PORT/" && break
  kill -0 "$DASH" 2>/dev/null || { echo "La dashboard non è partita."; pausa; exit 1; }
  sleep 1
done

open "$(harvey dashboard --url)"
echo
echo "  Harvey è acceso. La dashboard si è aperta nel browser."
echo "  Per spegnere tutto: chiudi questa finestra."
echo

wait "$DASH"
