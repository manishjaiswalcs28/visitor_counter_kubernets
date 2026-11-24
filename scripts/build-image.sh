#!/usr/bin/env bash
set -euo pipefail
PROFILE="${1:-visitor-primary}"
docker build -t visitor-counter:local .
minikube -p "$PROFILE" image load visitor-counter:local
echo "Loaded visitor-counter:local into $PROFILE"
