# TaskFlow Troubleshooting Guide

## Overview

This document provides troubleshooting procedures for the TaskFlow DevOps Platform.

The guide covers application, Docker, Kubernetes, Helm, AWS, Terraform, GitHub Actions, CI/CD, monitoring, security, networking, deployment, and rollback issues.
---

## 1. General Troubleshooting Approach

When an issue occurs, troubleshoot from the lowest layer upward:

Application
    ↓
Docker Image / Container
    ↓
Kubernetes Resources
    ↓
Helm Release
    ↓
AWS EC2 / ECR
    ↓
GitHub Actions CI/CD
    ↓
Monitoring

Start by identifying:
1. What component failed?
2. When did the failure occur?
3. Was the failure local or remote?
4. Did the failure occur during CI, CD, or runtime?
5. Was there a recent configuration or deployment change?
---

# 2. Application Troubleshooting

## Check Application Tests

Run the test suite locally:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

If tests fail, inspect the failing test and application logs before changing deployment configuration.

## Check Application Health

Verify the application health endpoint:

```bash
curl http://localhost:<PORT>/health
```

Verify metrics:

```bash
curl http://localhost:<PORT>/metrics
```

## Application Not Starting

Check the application directly:

```bash
python app/app.py
```

Check installed dependencies:

```bash
pip list
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Check for Python import errors:

```bash
python -c "import flask"
```
---

# 3. Docker Troubleshooting

## Check Docker

```bash
docker version
```
Check running containers:

```bash
docker ps
```
Check all containers:
```bash
docker ps -a
```
## Container Exits Immediately
Check container logs:

```bash
docker logs <container-id>
```
Inspect the container:
```bash
docker inspect <container-id>
```
## Image Build Failure

Build manually:

```bash
docker build -t taskflow-app:test .
```

Common causes:

* Incorrect Dockerfile instructions
* Missing application files
* Dependency installation failure
* Incorrect working directory
* Invalid requirements
* Incorrect application startup command

## Test Container Locally

```bash
docker run -d --name taskflow-test -p 5000:5000 taskflow-app:test
```

Check:

```bash
docker ps
docker logs taskflow-test
```

Test:

```bash
curl http://localhost:5000/health
```

Remove the test container:

```bash
docker rm -f taskflow-test
```

---

# 4. Docker Image Troubleshooting

List local images:

```bash
docker images
```

Inspect an image:

```bash
docker inspect <image>
```

Check image metadata:

```bash
docker image inspect <image>
```

If an image works locally but fails in Kubernetes, compare:

* Image tag
* Environment variables
* Container port
* Startup command
* Mounted configuration
* Kubernetes resource configuration

---

# 5. Trivy Troubleshooting

Run a local vulnerability scan:

```bash
trivy image <image>
```

Scan only high and critical vulnerabilities:

```bash
trivy image --severity HIGH,CRITICAL <image>
```

If the CI pipeline fails at Trivy:

1. Identify the affected package.
2. Check whether an updated base image is available.
3. Update dependencies where appropriate.
4. Rebuild the image.
5. Run Trivy again.
6. Commit the corrected image configuration.

Do not bypass a vulnerability check without understanding the finding.

---

# 6. Git Troubleshooting

Check repository state:

```bash
git status
```

Check recent commits:

```bash
git log --oneline --max-count=10
```

Check remote:

```bash
git remote -v
```

Update local branch:

```bash
git pull
```

Push changes:

```bash
git push origin main
```

If the working tree unexpectedly contains changes:

```bash
git status
git diff
```

Before committing, verify that generated files, virtual environments, credentials, and temporary files are excluded.

---

# 7. GitHub Actions CI Troubleshooting

Check the workflow execution in GitHub Actions.

The CI pipeline should be examined in this order:

Checkout
   ↓
Python Setup
   ↓
Dependencies
   ↓
Tests
   ↓
SonarQube
   ↓
Docker Build
   ↓
Trivy


## Test Failure

Run locally:

```bash
pytest -v
```

Fix application or test failures before rerunning CI.

## SonarQube Failure

Check:

* Project configuration
* Repository configuration
* SonarQube token
* Organization/project settings
* Quality gate result
* Source-code findings

Never commit the SonarQube token to the repository.

## Docker Build Failure in CI

Compare the CI environment with the local environment.

Check:

* Dockerfile
* Build context
* Required files
* Dependencies
* Build arguments
* Image tag

## Trivy Failure

Inspect the Trivy output and identify HIGH or CRITICAL findings.

Rebuild after remediation and rerun the scan.


# 8. GitHub Actions CD Troubleshooting

The CD pipeline generally follows:

AWS Authentication
       ↓
ECR Authentication
       ↓
Docker Build
       ↓
ECR Push
       ↓
EC2 Connection
       ↓
Helm Deployment
       ↓
Kubernetes Rollout

Identify which stage failed before troubleshooting the deployment itself.

---

# 9. AWS Authentication Troubleshooting

Verify that the GitHub Actions workflow has access to the required AWS credentials.

Common causes:

* Incorrect secret name
* Expired credentials
* Missing permissions
* Incorrect AWS region
* Incorrect account configuration

Never print AWS credentials in workflow logs.

Verify the configured region and account context.
---

# 10. Amazon ECR Troubleshooting

List ECR repositories:

```bash
aws ecr describe-repositories
```

List images:

```bash
aws ecr list-images --repository-name <repository>
```

Authenticate Docker with ECR:

```bash
aws ecr get-login-password --region <region> | \
docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
```
Common ECR problems:

* Incorrect repository name
* Incorrect AWS region
* Authentication failure
* Missing IAM permissions
* Incorrect image tag
* Image not pushed successfully

---

# 11. EC2 Troubleshooting

Check EC2 connectivity.

Verify:

* Instance is running
* Security Group rules
* SSH configuration
* Network connectivity
* Correct key
* Correct username
* Required services

Once connected:

```bash
uname -a
```
Check available resources:

```bash
free -h
df -h
```

Check CPU:

```bash
top
```

Check processes:

```bash
ps aux
```
Resource exhaustion can cause Kubernetes and monitoring components to become unstable.

---

# 12. Kubernetes Troubleshooting

Check cluster access:

```bash
kubectl cluster-info
```

Check nodes:

```bash
kubectl get nodes
```

Check namespaces:

```bash
kubectl get namespaces
```

Check TaskFlow resources:

```bash
kubectl get all -n taskflow
```

Check pods:

```bash
kubectl get pods -n taskflow
```

Check services:

```bash
kubectl get svc -n taskflow
```

---

# 13. Pod Not Running

Check pod status:

```bash
kubectl get pods -n taskflow
```

Describe the pod:

```bash
kubectl describe pod <pod-name> -n taskflow
```

Check logs:

```bash
kubectl logs <pod-name> -n taskflow
```

For previous container logs:

```bash
kubectl logs <pod-name> -n taskflow --previous
```

Common statuses:

* Pending
* ImagePullBackOff
* ErrImagePull
* CrashLoopBackOff
* Running
* Terminating

---

# 14. CrashLoopBackOff

Check logs:

```bash
kubectl logs <pod-name> -n taskflow
```

Describe the pod:

```bash
kubectl describe pod <pod-name> -n taskflow
```

Common causes:

* Application startup failure
* Missing configuration
* Invalid environment variable
* Missing secret
* Incorrect command
* Incorrect container port
* Dependency failure
* Resource constraints

Fix the underlying application or configuration issue instead of repeatedly restarting the pod.

---

# 15. ImagePullBackOff / ErrImagePull

Check pod events:

```bash
kubectl describe pod <pod-name> -n taskflow
```

Verify the configured image:

```bash
kubectl get deployment -n taskflow -o yaml
```

Check:

* ECR image exists
* Image tag is correct
* EC2 has ECR access
* Registry authentication is valid
* `imagePullSecrets` is correctly configured

Check the ECR registry secret:

```bash
kubectl get secret -n taskflow
```

---

# 16. Kubernetes Service Troubleshooting

List services:

```bash
kubectl get svc -n taskflow
```

Inspect the service:

```bash
kubectl describe svc <service-name> -n taskflow
```

Check endpoints:

```bash
kubectl get endpoints -n taskflow
```

If endpoints are empty, verify that the Service selector matches the pod labels.

---

# 17. Kubernetes Configuration Troubleshooting

Check ConfigMaps:

```bash
kubectl get configmap -n taskflow
```

Inspect a ConfigMap:

```bash
kubectl describe configmap <name> -n taskflow
```

Check Secrets:

```bash
kubectl get secrets -n taskflow
```

Do not expose secret values in logs or documentation.

---

# 18. Kubernetes Rollout Troubleshooting

Check rollout:

```bash
kubectl rollout status deployment/taskflow-taskflow-chart -n taskflow
```

Check rollout history:

```bash
kubectl rollout history deployment/taskflow-taskflow-chart -n taskflow
```

If rollout does not complete:

```bash
kubectl describe deployment taskflow-taskflow-chart -n taskflow
```

Then inspect the affected pods.

Common causes:

* Image pull failure
* Readiness failure
* Application startup failure
* Resource constraints
* Invalid configuration
* Scheduling failure

---

# 19. Terminating Pods

During a normal deployment, older pods may temporarily show:

```text
Terminating
```

This can occur while Kubernetes replaces old replicas with the new deployment.

Check:

```bash
kubectl get pods -n taskflow
```

If pods remain terminating unexpectedly, inspect:

```bash
kubectl describe pod <pod-name> -n taskflow
```

Do not force-delete pods unless the underlying issue is understood.

---

# 20. Helm Troubleshooting

List releases:

```bash
helm list -n taskflow
```

Check release history:

```bash
helm history taskflow -n taskflow
```

Check release status:

```bash
helm status taskflow -n taskflow
```

Inspect Helm values:

```bash
helm get values taskflow -n taskflow
```

Inspect rendered resources:

```bash
helm get manifest taskflow -n taskflow
```

---

# 21. Helm Upgrade Failure

If an upgrade fails:

```bash
helm history taskflow -n taskflow
```

Check the failed revision and its description.

Then inspect Kubernetes resources:

```bash
kubectl get pods -n taskflow
kubectl get events -n taskflow --sort-by=.lastTimestamp
```

A previous known-good release can be restored with:

```bash
helm rollback taskflow <REVISION> -n taskflow
```

Verify:

```bash
helm list -n taskflow
kubectl rollout status deployment/taskflow-taskflow-chart -n taskflow
```

---

# 22. Helm Release Not Found

If:

```bash
helm list
```

does not show the release, check the namespace.

Use:

```bash
helm list -n taskflow
```

Helm releases are namespace-scoped.

For TaskFlow, the correct namespace is:

```text
taskflow
```

Therefore:

```bash
helm history taskflow -n taskflow
```

must be used instead of:

```bash
helm history taskflow
```

---

# 23. Helm Template Validation

Before applying a Helm change, validate the chart:

```bash
helm lint taskflow-chart
```

Render the chart:

```bash
helm template taskflow taskflow-chart -n taskflow
```

These commands help identify YAML and template errors before deployment.

---

# 24. Helm Rollback Troubleshooting

Check available revisions:

```bash
helm history taskflow -n taskflow
```

Rollback:

```bash
helm rollback taskflow <REVISION> -n taskflow
```

Verify:

```bash
helm list -n taskflow
kubectl get pods -n taskflow
kubectl rollout status deployment/taskflow-taskflow-chart -n taskflow
```

A rollback should always be followed by application and workload verification.

---

# 25. Prometheus Troubleshooting

Check Prometheus pod:

```bash
kubectl get pods -n taskflow | grep prometheus
```

Check logs:

```bash
kubectl logs <prometheus-pod> -n taskflow
```

Check Prometheus service:

```bash
kubectl get svc -n taskflow
```

Common problems:

* Target is down
* Incorrect scrape configuration
* Application metrics endpoint unavailable
* Service discovery failure
* Network connectivity issue
* Prometheus resource exhaustion

---

# 26. Application Metrics Troubleshooting

Verify the application metrics endpoint:

```bash
curl http://<application-endpoint>/metrics
```

If `/metrics` is unavailable, check:

```bash
kubectl logs <taskflow-pod> -n taskflow
```

Verify the application service:

```bash
kubectl get svc -n taskflow
```

Verify the application pod:

```bash
kubectl get pods -n taskflow
```

---

# 27. Grafana Troubleshooting

Check Grafana:

```bash
kubectl get pods -n taskflow | grep grafana
```

Check logs:

```bash
kubectl logs <grafana-pod> -n taskflow
```

Check service:

```bash
kubectl get svc -n taskflow
```

Common problems:

* Grafana pod not running
* Service unavailable
* Prometheus datasource unavailable
* Dashboard queries returning no data
* Persistent storage problems

---

# 28. Grafana Dashboard Shows No Data

Check Prometheus first.

Verify:

```bash
kubectl get pods -n taskflow
```

Then verify Prometheus targets and metrics.

If Prometheus has no application metrics:

1. Verify TaskFlow `/metrics`.
2. Verify Prometheus scrape configuration.
3. Verify Service discovery.
4. Verify network connectivity.
5. Check Prometheus logs.

If Prometheus contains the metrics but Grafana does not display them:

1. Check the Grafana datasource.
2. Verify the datasource points to Prometheus.
3. Check dashboard queries.
4. Check the selected time range.

---

# 29. kube-state-metrics Troubleshooting

Check:

```bash
kubectl get pods -n taskflow | grep kube-state-metrics
```

Check logs:

```bash
kubectl logs <kube-state-metrics-pod> -n taskflow
```

Check service:

```bash
kubectl get svc -n taskflow | grep kube-state-metrics
```

If Kubernetes dashboard metrics are missing, verify that kube-state-metrics is running and reachable by Prometheus.

---

# 30. Grafana Persistence Troubleshooting

Check persistent resources:

```bash
kubectl get pvc -n taskflow
```

Check persistent volume:

```bash
kubectl get pv
```

Describe the PVC:

```bash
kubectl describe pvc <pvc-name> -n taskflow
```

Common causes:

* PVC not bound
* Incorrect storage configuration
* Volume mount issue
* Permission issue

Grafana persistence is important because pod recreation should not unnecessarily remove stored Grafana data.

---

# 31. Terraform Troubleshooting

Initialize Terraform:

```bash
terraform init
```

Validate configuration:

```bash
terraform validate
```

Format configuration:

```bash
terraform fmt
```

Review the plan:

```bash
terraform plan
```

Apply infrastructure:

```bash
terraform apply
```

Common problems:

* Incorrect working directory
* Missing AWS credentials
* Incorrect region
* Invalid resource configuration
* Missing IAM permissions
* Incorrect Terraform state configuration

Always run Terraform commands from the directory containing the Terraform configuration.

---

# 32. Terraform Working Directory Issue

If Terraform reports that configuration files cannot be found, verify the current directory:

```bash
pwd
ls
```

Then navigate to the Terraform configuration directory before running:

```bash
terraform plan
```

This avoids running Terraform from an unrelated project directory.

---

# 33. Terraform AWS Credentials

If Terraform cannot authenticate with AWS, verify:

```bash
aws sts get-caller-identity
```

If this command fails, AWS authentication must be corrected before Terraform can provision resources.

Do not commit AWS credentials to Git.

---

# 34. Networking Troubleshooting

For application connectivity problems, check the layers in order:

Pod
 ↓
Service
 ↓
Kubernetes Networking
 ↓
EC2
 ↓
AWS Security Group
 ↓
Client


Check pods:

```bash
kubectl get pods -n taskflow
```

Check services:

```bash
kubectl get svc -n taskflow
```

Check endpoints:

```bash
kubectl get endpoints -n taskflow
```

If the service has no endpoints, verify pod labels and Service selectors.

---

# 35. Resource Troubleshooting

Check resource usage:

```bash
kubectl top pods -n taskflow
```

Check nodes:

```bash
kubectl top nodes
```

If metrics are unavailable, verify that the required Kubernetes metrics components are installed and functioning.

Check EC2 resources:

```bash
free -h
df -h
top
```

Low memory or disk space can affect Kubernetes, Prometheus, Grafana, and application stability.

---

# 36. HPA Troubleshooting

Check HPA:

```bash
kubectl get hpa -n taskflow
```

Describe it:

```bash
kubectl describe hpa -n taskflow
```

Check current replicas:

```bash
kubectl get deployment -n taskflow
```

If HPA does not scale as expected, verify:

* Resource requests are configured.
* Metrics are available.
* HPA configuration is valid.
* The deployment is healthy.

---

# 37. Secret Troubleshooting

Check available secrets:

```bash
kubectl get secrets -n taskflow
```

Check secret metadata:

```bash
kubectl describe secret <secret-name> -n taskflow
```

Do not expose secret values using commands or screenshots.

If an image pull secret is not working, verify:

* Secret exists in the correct namespace.
* Secret name matches the deployment.
* Registry credentials are valid.
* ECR repository and region are correct.

---

# 38. Configuration Troubleshooting

Check ConfigMaps:

```bash
kubectl get configmaps -n taskflow
```

Inspect:

```bash
kubectl describe configmap <configmap-name> -n taskflow
```

After changing configuration through Helm, verify that the updated pods receive the expected configuration.

---

# 39. Deployment Failure Investigation

When a deployment fails, collect the following information:

```bash
helm status taskflow -n taskflow
helm history taskflow -n taskflow
kubectl get pods -n taskflow
kubectl get deployments -n taskflow
kubectl get svc -n taskflow
kubectl get events -n taskflow --sort-by=.lastTimestamp
```

Then inspect the affected pod:

```bash
kubectl describe pod <pod-name> -n taskflow
kubectl logs <pod-name> -n taskflow
```

This provides enough information to determine whether the failure is related to:

* Image
* Configuration
* Application
* Kubernetes
* Networking
* Resources
* Helm
* AWS

---

# 40. Context Deadline Exceeded During Helm Upgrade

A Helm upgrade may fail with:

```text
context deadline exceeded
```

Possible causes include:

* Pods failing to become ready
* Image pull problems
* Application startup failure
* Insufficient EC2 resources
* Kubernetes scheduling problems
* Readiness probe failures
* Network problems

Investigate:

```bash
kubectl get pods -n taskflow
kubectl describe pods -n taskflow
kubectl get events -n taskflow --sort-by=.lastTimestamp
```

Check Helm history:

```bash
helm history taskflow -n taskflow
```

If the previous release is known to be healthy, rollback can be performed.

---

# 41. CI/CD Deployment Recovery

If CI succeeds but CD fails:

```text
CI
 ↓
Image Available?
 ↓
ECR
 ↓
EC2 Connectivity
 ↓
Kubernetes Access
 ↓
Helm
 ↓
Rollout
```

Check the first failed stage instead of rerunning the entire process blindly.

If the image was successfully pushed but deployment failed, verify the ECR image and Kubernetes configuration before rerunning deployment.

---

# 42. Useful Diagnostic Command Set

For a quick overall health check:

```bash
kubectl get nodes
kubectl get all -n taskflow
kubectl get pods -n taskflow
kubectl get svc -n taskflow
kubectl get hpa -n taskflow
helm list -n taskflow
helm status taskflow -n taskflow
helm history taskflow -n taskflow
```

Check recent Kubernetes events:

```bash
kubectl get events -n taskflow --sort-by=.lastTimestamp
```
---

# 43. Final Troubleshooting Checklist

Before considering an incident resolved, verify:

* [ ] Application is healthy.
* [ ] Application tests pass.
* [ ] Docker image builds successfully.
* [ ] Trivy scan passes according to configured policy.
* [ ] SonarQube analysis completes successfully.
* [ ] Docker image exists in Amazon ECR.
* [ ] EC2 environment is reachable.
* [ ] Kubernetes nodes are healthy.
* [ ] TaskFlow pods are running.
* [ ] TaskFlow Service has endpoints.
* [ ] Helm release status is `deployed`.
* [ ] Prometheus is running.
* [ ] Grafana is running.
* [ ] kube-state-metrics is running.
* [ ] Application metrics are available.
* [ ] Grafana dashboards display expected metrics.
* [ ] Deployment rollout completes successfully.
* [ ] Rollback procedure remains available.

---

## Conclusion

TaskFlow troubleshooting follows a layered approach across application, container, Kubernetes, Helm, AWS, CI/CD, infrastructure, and monitoring components.

The primary objective is to identify the failing layer, collect evidence using logs and resource status, correct the underlying issue, and verify the complete deployment after recovery.
