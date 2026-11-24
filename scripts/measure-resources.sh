#!/usr/bin/env bash
set -euo pipefail
kubectl top pods -n visitor-system || true
echo
kubectl get deployment visitor-web -n visitor-system \
  -o jsonpath='Replicas desired={.spec.replicas}{"\n"}CPU request per pod={.spec.template.spec.containers[0].resources.requests.cpu}{"\n"}Memory request per pod={.spec.template.spec.containers[0].resources.requests.memory}{"\n"}CPU limit per pod={.spec.template.spec.containers[0].resources.limits.cpu}{"\n"}Memory limit per pod={.spec.template.spec.containers[0].resources.limits.memory}{"\n"}'
