#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-visitor-secondary}"
if [[ "$TARGET" != "visitor-primary" && "$TARGET" != "visitor-secondary" ]]; then
  echo "Usage: $0 [visitor-primary|visitor-secondary]"; exit 1
fi
kubectl config use-context "$TARGET"
echo "Traffic target switched to simulated environment: $TARGET"
echo "Service URL:"
minikube service visitor-web -n visitor-system -p "$TARGET" --url
echo "Verify /health and /api/stats at the URL above."
