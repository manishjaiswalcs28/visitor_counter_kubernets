#!/usr/bin/env bash
set -euo pipefail
PROFILE="${1:-visitor-primary}"
kubectl config use-context "$PROFILE"
./scripts/build-image.sh "$PROFILE"
kubectl apply -f k8s.yaml
kubectl rollout status deployment/redis -n visitor-system --timeout=120s
kubectl rollout status deployment/visitor-web -n visitor-system --timeout=180s
kubectl apply -f k8s/hpa.yaml
echo "Deployment complete on $PROFILE"
kubectl get pods,svc,hpa -n visitor-system
