#!/usr/bin/env bash
set -euo pipefail
# Two local Minikube profiles simulate private and public-cloud environments.
minikube start -p visitor-primary --driver=docker --cpus=2 --memory=3072
minikube start -p visitor-secondary --driver=docker --cpus=2 --memory=3072
minikube addons enable metrics-server -p visitor-primary
minikube addons enable metrics-server -p visitor-secondary
echo "Created local simulation clusters: visitor-primary and visitor-secondary"
