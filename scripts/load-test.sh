#!/usr/bin/env bash
set -euo pipefail
URL="${1:?Usage: ./scripts/load-test.sh http://SERVICE:5000}"
DURATION="${2:-180}"
echo "Sending concurrent requests to $URL for ${DURATION}s"
if command -v hey >/dev/null 2>&1; then
  hey -z "${DURATION}s" -c 40 "$URL/"
else
  echo "Install hey for a controlled load test, or run:"
  echo "kubectl run -n visitor-system loadgen --rm -it --restart=Never --image=busybox -- sh -c 'i=0; while [ \$i -lt 5000 ]; do wget -q -O- $URL/ >/dev/null; i=\$((i+1)); done'"
fi
