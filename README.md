# oc-prometheus

A lightweight **Prometheus + Grafana** stack for monitoring MacStadium Orka
clusters using vendor-supported Prometheus metrics — no Kubernetes access required.

## Features
- **One file to configure** — set your IP plan in `.env`, that's it
- Preconfigured **"Orka — Customer Overview"** dashboard (health, capacity, deploy success, network throughput, per-node bar gauges)
- Node names, cluster identity, and metrics all populate automatically
- Runs anywhere Docker does (laptop or a host)

## Requirements
- Docker + Docker Compose
- Network access to your Orka private IP plan (e.g. over VPN)

## Setup
```bash
cp env.example .env
# Edit .env — set ORKA_ENDPOINT, ORKA_NODE_EXPORTERS, and the CLUSTER_NAME/ORKA_VERSION/TENANT
docker compose up -d
```
On `up`, a small `config-init` step generates `prometheus/prometheus.yml` from your
`.env` (Prometheus can't read env vars itself), then Prometheus + Grafana start.
Re-run `docker compose up -d` after editing `.env` to regenerate.

## Access
- **Grafana:** http://localhost:3000  (admin / admin — set in `.env`) → dashboard **"Orka — Customer Overview"**
- **Prometheus:** http://localhost:9090

## How it fits together
- `.env` — the only file you edit: IP plan + cluster identity
- `prometheus/generate-config.sh` — renders `prometheus.yml` from `.env` at start-up
- The dashboard reads **cluster / version / tenant** from Prometheus scrape labels and
  **node names live** from each exporter's `node_uname_info` — so it works for any cluster with no dashboard edits

## Notes
- Metrics are scraped from the Orka operator (`:8080`) and node exporters (`:9100`)
- This project does not modify the Orka cluster
- `prometheus/prometheus.yml` is generated (gitignored); edit `.env`, not that file
