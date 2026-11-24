# Report writing guide

Use this as the structure for your own practical report. Add your name, roll number, dates, terminal screenshots and measured results.

1. Cover page — project title, student details, course, GitHub URL.
2. Aim — deploy a Redis-backed visitor counter using containers and Kubernetes.
3. Tools — Docker Desktop, Minikube, kubectl, Flask, Redis, Python.
4. Architecture — insert `docs/architecture.svg`; explain primary and secondary local clusters.
5. Task A — Dockerfile, Compose, build/run commands and app screenshot.
6. Task B — Kubernetes objects, pods/services and self-healing evidence.
7. Task C — HPA configuration, metrics-server, load test and replica change screenshot.
8. Task D — explain the two Minikube profiles as a local hybrid-cloud simulation; show primary stopped and secondary serving traffic. Clearly state Redis data is not replicated and failover is manually switched.
9. Task E — show at least three optimization techniques and your measured before/after table. Do not claim estimated values as measured values.
10. Result, limitations and conclusion.
11. GitHub repository link.

## Cost comparison table to complete with your own measurements

| Optimization | Before | After | Evidence |
|---|---:|---:|---|
| CPU request per web pod | Measure baseline | 100m | Deployment YAML |
| Memory request per web pod | Measure baseline | 96Mi | Deployment YAML |
| Idle replica count | Measure fixed-replica baseline | HPA minimum 2 | `kubectl get hpa` |
| Container image size | Measure heavier baseline | Measure slim image | `docker image ls` |

The figures shown as configuration targets are not proof of savings. Add the actual measured before/after values and describe the measurement method.
