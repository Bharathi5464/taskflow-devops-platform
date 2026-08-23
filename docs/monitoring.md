# TaskFlow Monitoring & Grafana Documentation

## Overview

TaskFlow uses Prometheus and Grafana for application and Kubernetes monitoring.

The monitoring stack collects application metrics, Kubernetes object metrics, and infrastructure-related metrics and presents them through Grafana dashboards.

## Monitoring Architecture


TaskFlow Application
        │
        │ /metrics
        ▼
   Prometheus
        │
        ▼
     Grafana


Kubernetes
        │
        ▼
kube-state-metrics
        │
        ▼
   Prometheus
        │
        ▼
     Grafana

## Monitoring Components

### Prometheus

Prometheus collects and stores metrics from:

* TaskFlow application
* Kubernetes workloads
* kube-state-metrics
* Configured monitoring targets

### Grafana

Grafana provides dashboards for visualizing the collected metrics.

### kube-state-metrics

kube-state-metrics exposes Kubernetes object and workload state metrics for Prometheus.

## Grafana Dashboards

### TaskFlow Application Overview

The dashboard provides visibility into application-level metrics, including:

* Application health
* HTTP request rate
* Total HTTP requests
* HTTP status codes
* P95 request latency
* Average request duration
* Python CPU usage
* Python memory usage
* Open file descriptors

### Monitoring System Health

The dashboard provides visibility into Prometheus monitoring health, including:

* Prometheus targets up
* Prometheus targets down
* Target health
* Scrape duration
* Active metrics

### Kubernetes & Infrastructure Overview

The dashboard provides Kubernetes and infrastructure visibility, including:

* Pod status
* CPU utilization
* Memory utilization
* Kubernetes workload state
* Cluster-level resource information

## Monitoring Verification

Verify Prometheus:

```bash
kubectl get pods -n taskflow
```

Verify Grafana:

```bash
kubectl get pods -n taskflow
```

Verify monitoring services:

```bash
kubectl get svc -n taskflow
```

Verify kube-state-metrics:

```bash
kubectl get pods -n taskflow | grep kube-state-metrics
```

## Grafana Persistence

Grafana uses persistent storage so dashboard and Grafana data can survive application pod recreation.

The Grafana persistent volume configuration is managed through the TaskFlow Helm chart.

## Monitoring Validation

Prometheus, Grafana, and kube-state-metrics have been deployed successfully and verified as part of the TaskFlow monitoring stack.

The Grafana dashboards have been created and validated against the available application and Kubernetes metrics.
