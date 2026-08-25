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

## Metrics explained

Tiles derive from Orka **operator** counters/histograms (`:8080`) and **node-exporter** metrics (`:9100`).

**Deploy Success Rate** — lifetime %
```
successes / (successes + failures) * 100
```
`orka_operator_virtual_machine_successes_total` / `_failures_total` are cumulative counters (reset if the operator restarts). This is an all-time ratio, so it's stable and moves slowly.

**Deploy Failures (24h)**
```
increase(orka_operator_virtual_machine_failures_total[24h])
```
A rolling 24-hour window of failed deploys (recent, unlike the lifetime success rate). Thresholds: green 0 · amber ≥1 · red ≥5.

**Avg Deploy Time** — seconds/deploy
```
sum(..._success_deployment_duration_seconds_sum) / clamp_min(sum(..._count), 1)
```
The operator records a histogram of successful-deploy durations; `sum ÷ count` = average. `clamp_min(count, 1)` only guards divide-by-zero before the first deploy.
> Pitfall: a windowed `rate(sum)/rate(count)` also works, but **never `clamp_min` the rate to 1** — a healthy deploy rate is well under 1/s, so clamping it forces the denominator to 1 and collapses the average toward zero.

**Running VMs** — `sum(orka_operator_virtual_machine_instances_total)`

**Per-node metrics** (bar gauges/table):
- CPU % — `100 - avg by (instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100`
- Network In/Out — `sum by (instance)(rate(node_network_{receive,transmit}_bytes_total[5m])) * 8` (bits/sec)
- Node names — joined live from `node_uname_info` via `group_left(nodename)`

## Notes
- Metrics are scraped from the Orka operator (`:8080`) and node exporters (`:9100`)
- This project does not modify the Orka cluster
- `prometheus/prometheus.yml` is generated (gitignored); edit `.env`, not that file
