#!/usr/bin/env bash
# Regressão por mock (sem FLAC3D): roda cada cenário com o itasca falso e compara com
# tests/baselines/<cenario>.log.
#
#   ./tests/regressao.sh            # compara
#   ./tests/regressao.sh --gravar   # atualiza as linhas de base (só depois de revisar a mudança)
set -u
cd "$(dirname "$0")/.."

PY="${PYTHON:-python3}"
CENARIOS="diagnostico diagnostico_sem_itasca extrair"
GRAVAR=0
[ "${1:-}" = "--gravar" ] && GRAVAR=1

mkdir -p tests/baselines
falhas=0
"$PY" tests/compat36.py || falhas=$((falhas + 1))
for c in $CENARIOS; do
  saida="$("$PY" tests/mock/rodar.py "$c" 2>&1)"
  base="tests/baselines/$c.log"
  if [ "$GRAVAR" = 1 ]; then
    printf '%s\n' "$saida" > "$base"
    echo "gravado  $c"
  elif [ ! -f "$base" ]; then
    echo "SEM BASE $c (rode com --gravar)"
    falhas=$((falhas + 1))
  elif diff -u "$base" <(printf '%s\n' "$saida") > /dev/null; then
    echo "ok       $c"
  else
    echo "MUDOU    $c"
    diff -u "$base" <(printf '%s\n' "$saida") | head -40
    falhas=$((falhas + 1))
  fi
done

if [ "$falhas" -gt 0 ]; then
  echo "$falhas cenário(s) com diferença."
  exit 1
fi
echo "Regressão OK."
