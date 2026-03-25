# oc-prometheus
oc-prometheus is a lightweight Prometheus + Grafana stack for monitoring
MacStadium Orka clusters using vendor-supported Prometheus metrics.

## Features
- One-command setup
- Prometheus-based metrics
- Preconfigured Grafana dashboards
- No Kubernetes access required

## Requirements
- Docker
- Docker Compose
- Network access to the Orka private IP plan

## Setup
```bash
cp env.example .env
# Edit ORKA_ENDPOINT and ORKA_NODE_EXPORTERS
docker compose up -d
```

## Access
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

## Default Login
- Username: admin
- Password: admin

## Notes
- Orka metrics are scraped from the Orka API, operator, and node exporters
- This project does not modify the Orka cluster
