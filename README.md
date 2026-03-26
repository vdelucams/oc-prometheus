# oc-prometheus
oc-prometheus is easy to start lightweight Prometheus + Grafana stack pre-set overview on 
MacStadium Orka clusters using vendor-supported Prometheus metrics.

## Features
- One-command setup
- Prometheus-based metrics
- Preconfigured Grafana dashboards
- No Kubernetes access required

## Requirements
- Docker
- Docker Compose
- Network access to Orka Cluster & IP plan

## Setup
```bash

# Edit ORKA_ENDPOINT and ORKA_NODE_EXPORTERS based on your IP Plan
#  Add IPs on prometheus.yml as example (update ips based on cluster IP Plan)

cp env.example .env 
docker compose up -d
```

## Access
- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090

## Default Login
- Username: admin
- Password: admin

## Notes
- Docker box must have visibility to Orka Cluster 
- Orka metrics are scraped from the Orka API, operator, and node exporters
- This project does not modify the Orka cluster
- You can create, use and modify the dashboards based on the MacStadium Orka Prometheus scraping and your needs.
- 
