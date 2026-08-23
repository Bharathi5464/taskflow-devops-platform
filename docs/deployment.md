# TaskFlow Deployment Documentation

## Overview

TaskFlow is deployed to a Kubernetes environment running on AWS EC2. The deployment process is automated through GitHub Actions and uses Amazon ECR for container image storage and Helm for Kubernetes release management.

## Deployment Flow

GitHub
   ↓
GitHub Actions
   ↓
Docker Build
   ↓
Amazon ECR
   ↓
AWS EC2
   ↓
Kubernetes
   ↓
Helm
   ↓
TaskFlow Application

## Deployment Process

The CD pipeline performs the following steps:

1. Authenticate with AWS.
2. Authenticate with Amazon ECR.
3. Build the Docker image.
4. Tag the image using the CI commit SHA.
5. Push the image to Amazon ECR.
6. Connect to the EC2 deployment environment.
7. Authenticate with the Kubernetes cluster.
8. Update the TaskFlow Helm release.
9. Wait for Kubernetes deployments to complete rollout.
10. Verify the deployment status.

## Helm Deployment

The TaskFlow application and monitoring components are deployed through the Helm chart.

The release includes:

* TaskFlow application
* TaskFlow Service
* Prometheus
* Grafana
* kube-state-metrics
* Grafana persistent storage
* Configuration and secrets
* Horizontal Pod Autoscaler

The Helm release is maintained in the `taskflow` namespace.

## Deployment Verification

Verify the Kubernetes workloads:

```bash
kubectl get pods -n taskflow
```

Verify the application rollout:

```bash
kubectl rollout status deployment/taskflow-taskflow-chart -n taskflow
```

Verify the Helm release:

```bash
helm list -n taskflow
```

Verify the Helm release history:

```bash
helm history taskflow -n taskflow
```

## Successful Deployment

A deployment is considered successful when:

* The Helm release status is `deployed`.
* TaskFlow application pods are `Running`.
* Prometheus is running.
* Grafana is running.
* kube-state-metrics is running.
* Kubernetes deployments complete successfully.
* The application is available through the configured Kubernetes service.

## Deployment Validation

The deployment process has been successfully tested through the CI/CD pipeline.

The current Helm release and Kubernetes workloads have been verified after deployment.
