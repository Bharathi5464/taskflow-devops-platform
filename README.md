# TaskFlow — End-to-End DevOps Platform

A Flask REST API deployed through an automated DevOps pipeline using containerization, Kubernetes, Infrastructure as Code, CI/CD, DevSecOps, and monitoring.


## Overview

TaskFlow demonstrates an end-to-end application delivery workflow covering application development, containerization, infrastructure provisioning, Kubernetes deployment, CI/CD automation, security validation, monitoring, and rollback.

**Core capabilities:**

* Application containerization with Docker
* Kubernetes deployment managed through Helm
* CI/CD automation with GitHub Actions
* Infrastructure as Code with Terraform
* DevSecOps validation with Trivy and SonarQube
* Monitoring and observability with Prometheus and Grafana
* Deployment and rollback testing

---

## Architecture

**Application delivery flow:**

Developer → GitHub → GitHub Actions → Docker → Amazon ECR → AWS EC2 → Kubernetes → Helm → TaskFlow Application

**Monitoring flow:**

TaskFlow /metrics → Prometheus → Grafana
Kubernetes → kube-state-metrics → Prometheus → Grafana

---

## Technology Stack

| Category               | Tools                                    |
| ---------------------- | ---------------------------------------- |
| Application            | Python, Flask, prometheus_flask_exporter |
| Containerization       | Docker                                   |
| Orchestration          | Kubernetes, Helm                         |
| Cloud & Infrastructure | AWS EC2, Amazon ECR, Terraform           |
| CI/CD                  | GitHub Actions                           |
| Security               | Trivy, SonarQube                         |
| Monitoring             | Prometheus, Grafana, kube-state-metrics  |
| OS / Scripting         | Linux, Bash                              |

---

## Application

TaskFlow is a Flask REST API providing health-check and task-management endpoints.

The application includes an automated test suite covering application and endpoint behavior and exposes Prometheus-compatible metrics through `/metrics`.

The application is packaged as a Docker image for deployment.


## Docker

The application is containerized using Docker.

The image build workflow includes:

* Dockerfile-based build
* Dependency installation
* Application packaging
* Container execution and local validation
* Vulnerability scanning with **Trivy**

Docker images are built through the CI pipeline and published to Amazon ECR.


## Kubernetes

TaskFlow runs on Kubernetes with the following components:

* Deployment
* Service
* ConfigMap
* Secret
* ServiceAccount
* Horizontal Pod Autoscaler (HPA)
* Prometheus
* Grafana with persistent storage
* kube-state-metrics

Application and monitoring components are managed declaratively through Helm.


## Helm

A Helm chart manages the TaskFlow application and monitoring stack.

Helm manages:

* Application deployment and service
* Configuration and secrets
* Horizontal Pod Autoscaler
* Prometheus
* Grafana and persistent storage
* kube-state-metrics
* Kubernetes monitoring configuration

Helm is integrated into the CD pipeline to provide versioned and repeatable deployments.


## AWS Deployment

* **Amazon ECR** — container image registry
* **AWS EC2** — Kubernetes runtime environment
* **Terraform** — infrastructure provisioning

**Deployment flow:**

GitHub Actions → Amazon ECR → AWS EC2 → Kubernetes → Helm → TaskFlow


---

## CI Pipeline

The CI pipeline performs:

1. Source code checkout
2. Python environment setup
3. Dependency installation
4. Automated test execution
5. SonarQube analysis
6. Docker image build
7. Trivy vulnerability scanning

The pipeline validates application code and the container image before deployment.

---

## CD Pipeline

The CD pipeline performs:

1. AWS authentication
2. Amazon ECR authentication
3. Docker image build and tagging
4. Image push to Amazon ECR
5. Deployment to the EC2 environment
6. Helm upgrade/install
7. Kubernetes rollout verification

A successful pipeline deploys the updated TaskFlow application to Kubernetes.

---

## DevSecOps

Security and code-quality validation are integrated into the CI pipeline.

* **Trivy** — scans Docker images for known vulnerabilities.
* **SonarQube** — performs static code analysis covering code quality, maintainability, and security-related findings.

---

## Monitoring & Observability

* **Prometheus** — collects application and Kubernetes metrics.
* **Grafana** — visualizes collected metrics through dashboards.
* **kube-state-metrics** — exposes Kubernetes object state metrics to Prometheus.

### Grafana Dashboards

**TaskFlow Application Overview**

Provides visibility into:

* Application health
* HTTP request rate
* Total requests
* HTTP status codes
* P95 request latency
* Average request duration
* Python CPU usage
* Python memory usage
* Open file descriptors

**Monitoring System Health**

Provides visibility into:

* Prometheus target status
* Target health
* Scrape duration
* Active metrics

**Kubernetes & Infrastructure Overview**

Provides visibility into Kubernetes and infrastructure resource metrics, including CPU, memory, and pod status.

---

## Deployment Verification

```bash
kubectl get pods -n taskflow

kubectl rollout status deployment/taskflow-taskflow-chart -n taskflow

helm list -n taskflow
```

A deployment is considered successful when the Helm release is in `deployed` status and the Kubernetes workloads complete their rollout successfully.

---

## Rollback

Helm maintains release history and supports recovery to a previous release revision.

View release history:

```bash
helm history taskflow -n taskflow
```

Rollback to a specific revision:

```bash
helm rollback taskflow <REVISION> -n taskflow
```

Verify the rollout after rollback:

```bash
kubectl rollout status deployment/taskflow-taskflow-chart -n taskflow
```

Rollback has been tested and successfully verified.

---

## Troubleshooting

Common troubleshooting commands:

```bash
kubectl get pods -n taskflow

kubectl get svc -n taskflow

kubectl describe pod <pod-name> -n taskflow

kubectl logs <pod-name> -n taskflow

helm list -n taskflow

helm history taskflow -n taskflow
```

These commands can be used to investigate application, Kubernetes, Helm, and deployment issues.

---

## Project Validation

| Component                                | Status |
| ---------------------------------------- | ------ |
| Flask application & automated tests      | ✅      |
| Docker containerization & Trivy scanning | ✅      |
| Kubernetes deployment                    | ✅      |
| Helm chart implementation                | ✅      |
| AWS EC2 deployment                       | ✅      |
| Amazon ECR integration                   | ✅      |
| Terraform infrastructure                 | ✅      |
| CI pipeline                              | ✅      |
| CD pipeline                              | ✅      |
| Prometheus monitoring                    | ✅      |
| Grafana dashboards                       | ✅      |
| kube-state-metrics                       | ✅      |
| Successful deployment testing            | ✅      |
| Rollback testing                         | ✅      |
| Documentation                            | ✅      |

---


