# LOOP — Visitor Counter (Flask + Redis + Docker + Kubernetes)

A small, visually distinctive visitor observatory built for the five project tasks.

## Stack
- Flask + Gunicorn web application
- Redis counter store
- Docker image and Docker Compose
- Kubernetes Deployment, Service, probes and HPA
- Two local Minikube profiles for a documented failover simulation

## 1. Run with Docker Compose
```bash
docker compose up --build
```
Open http://localhost:5001. Each refresh increments the Redis-backed count.
Health: http://localhost:5001/health ; JSON stats: http://localhost:5001/api/stats

Stop:
```bash
docker compose down
```
To also remove stored counter data:
```bash
docker compose down -v
```

## 2. Create two local Kubernetes clusters
Prerequisites: Docker Desktop, kubectl, Minikube.
```bash
chmod +x scripts/*.sh
./scripts/create-clusters.sh
```
This creates `visitor-primary` and `visitor-secondary`. Both are on your laptop and simulate two cloud environments.

## 3. Deploy to primary
```bash
./scripts/deploy.sh visitor-primary
minikube service visitor-web -n visitor-system -p visitor-primary --url
```
Open the URL printed. Check:
```bash
kubectl get pods,svc,hpa -n visitor-system
kubectl get deployment visitor-web -n visitor-system
kubectl get hpa -n visitor-system
```

## 4. Self-healing demonstration
```bash
kubectl get pods -n visitor-system
kubectl delete pod -n visitor-system -l app=visitor-web
kubectl get pods -n visitor-system -w
```
Capture the deleted pod and its replacement becoming Ready. Deployment desired replicas should return to the configured count.

## 5. HPA demonstration
Metrics Server is enabled by the cluster creation script.
```bash
kubectl top pods -n visitor-system
kubectl get hpa -n visitor-system -w
```
In another terminal, obtain the service URL and generate traffic. Install `hey` if available (`brew install hey` on macOS), then:
```bash
./scripts/load-test.sh http://<service-url> 240
```
For a Minikube service URL with a port, pass the complete URL. Watch HPA and pods:
```bash
kubectl get hpa,pods -n visitor-system -w
```
Scaling may take a minute or two. CPU requests are set on the web containers because HPA CPU utilization is calculated relative to requests.

## 6. Secondary deployment and failover simulation
Deploy the same app to the second local cluster:
```bash
./scripts/deploy.sh visitor-secondary
```
Check that it responds:
```bash
minikube service visitor-web -n visitor-system -p visitor-secondary --url
```
Simulate primary outage by stopping the primary cluster:
```bash
minikube stop -p visitor-primary
./scripts/failover.sh visitor-secondary
```
Open the secondary URL printed by the script and verify `/health` and the home page. This demonstrates a manual traffic/endpoint switch to a standby environment.
Restore primary:
```bash
minikube start -p visitor-primary
```

**Important limitation:** the two Minikube clusters are independent and their Redis stores are not replicated. The secondary app remains available, but its visitor count is separate and may start at zero. This is a local failover simulation, not production-grade cross-cloud data replication or automatic DNS failover.

## 7. Cost optimization — collect actual measurements
Do not invent values. Run the baseline and optimized experiments yourself and fill `docs/cost-analysis-template.csv` with measured results and screenshots.

Three implemented optimization techniques:
1. **Resource right-sizing:** CPU/memory requests and limits are explicitly bounded (web: request 100m/96Mi, limit 500m/256Mi; Redis: request 50m/64Mi, limit 250m/192Mi). Compare with a baseline manifest using larger requests, then measure `kubectl top pods`.
2. **HPA instead of permanently over-provisioned replicas:** set a baseline fixed replica count (for example 5) and record idle pod count; apply HPA with minimum 2 and maximum 8, then record idle count and load-test scale-up. Explain that HPA saves idle capacity but adds pods under load.
3. **Lean container/runtime:** use `python:3.12-slim`, install only pinned runtime dependencies, disable pip cache, and run as a non-root user. Compare image size with a deliberately heavier baseline such as `python:3.12` built from the same app and dependencies. Record `docker image ls` output.

Measurement commands:
```bash
kubectl top pods -n visitor-system
kubectl get hpa -n visitor-system
kubectl get deploy visitor-web -n visitor-system -o yaml
docker image ls visitor-counter
```
For a fair before/after comparison, keep the test duration, traffic rate and laptop conditions similar. These are local resource/image measurements, not actual cloud-billing savings. State this in your report.

## Deliverables checklist
- Source: `app.py`, `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `k8s.yaml`, `k8s/hpa.yaml`
- Screenshots: Compose app, Kubernetes pods/services, self-healing, HPA scale-up, secondary cluster, failover after primary stop, cost measurements
- Architecture diagram: `docs/architecture.svg`
- Cost analysis: completed `docs/cost-analysis-template.csv` plus explanation in report
- GitHub: public repository URL in `github_link.txt`
- ZIP: upload the GitHub **Code → Download ZIP** archive to the class Drive folder

## Clean up
```bash
minikube delete -p visitor-primary
minikube delete -p visitor-secondary
docker compose down -v
```
