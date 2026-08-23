# TaskFlow Rollback Documentation

## Overview

TaskFlow uses Helm release history to support controlled rollback to a previously deployed application version.

Rollback allows a previous known release to be restored when a deployment requires recovery.

## View Release History

List the available Helm revisions:

```bash
helm history taskflow -n taskflow
```

Example:

```text 
REVISION   STATUS       DESCRIPTION
1          superseded   Install complete
2          failed       Upgrade failed
3          superseded   Rollback to 1
4          superseded   Upgrade complete
5          superseded   Upgrade complete
6          deployed     Upgrade complete
```

## Perform Rollback

Rollback the release to a selected revision:

```bash 
helm rollback taskflow <REVISION> -n taskflow
```

Example:

```bash 
helm rollback taskflow 5 -n taskflow
```

## Verify Rollback

Check the Helm release:

```bash 
helm list -n taskflow
```

Check the release history:

```bash 
helm history taskflow -n taskflow
```

Verify the Kubernetes rollout:

```bash 
kubectl rollout status deployment/taskflow-taskflow-chart -n taskflow
```

Check the running workloads:

```bash 
kubectl get pods -n taskflow
```

## Rollback Validation

A Helm rollback has been tested in the TaskFlow environment.

The rollback process successfully restored a previous release and the Kubernetes deployment was subsequently verified.

## Recovery Process

The standard recovery sequence is:

Identify deployment issue
        ↓
Check Helm release history
        ↓
Select known-good revision
        ↓
Execute Helm rollback
        ↓
Verify Kubernetes rollout
        ↓
Verify application availability

