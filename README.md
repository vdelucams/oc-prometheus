# oc-prometheus

A lightweight **Prometheus + Grafana** stack for monitoring MacStadium Orka
clusters using vendor-supported Prometheus metrics — no Kubernetes access required.

## Features
- **One file to configure** — set your IP plan in `.env`, that's it
- Preconfigured **"Orka — Customer Overview"** dashboard (health, capacity, deploy success, network throughput, per-node bar gauges)
- Optional **VM slot capacity** (kube-state-metrics), **firewall SNMP** (Cisco ASA/ASAv) and a **customer-consumable metrics example** dashboard, see below
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

## Pointing it at your own cluster or lab

Everything the stack scrapes is on the cluster's **private network**, so run it on a
machine that is on that network: a laptop connected to the cluster VPN, or a host
inside the firewall. Nothing is installed on the cluster.

| `.env` value | What it is | Where to find it |
|---|---|---|
| `ORKA_ENDPOINT` | Host that serves the Orka **operator** metrics on `:8080/metrics` | The Orka load-balancer address, listed in the **IP Allocation** table of **My Cloud** in the MacStadium Portal (standard plan: `x.x.x.20`) |
| `ORKA_NODE_EXPORTERS` | Every Orka node, `ip:9100` | **Host Assignments** in My Cloud, or `orka3 node list` (standard plan: `x.x.x.31` upwards) |
| `CLUSTER_NAME`, `ORKA_VERSION`, `TENANT`, `SITE` | Labels shown in the dashboard header | Your cluster name (`ORK…`), `orka3 version`, your MS number, data centre |
| `FW_SNMP_TARGET` (optional) | The firewall's **inside** address | Gateway of your private subnet in the IP Allocation table |

Check reachability before starting (both should answer):
```bash
curl -sI http://<ORKA_ENDPOINT>:8080/metrics | head -1
curl -sI http://<node-ip>:9100/metrics | head -1
```
The public page [Consuming Metrics from Prometheus](https://docs.macstadium.com/orka/orka-resources/consuming-metrics-from-prometheus)
documents the operator `:8080/metrics` and node-exporter `:9100/metrics` endpoints and
notes that port 9100 must accept TCP from the host running Prometheus. The optional
**kube-state-metrics** feed used by the VM Slot Capacity and Customer X dashboards is not
on that page; this repo reaches it with the `ksm-tunnel` container and a kubeconfig.

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

## Optional: VM Slot Capacity dashboard (kube-state-metrics)

The **"Orka — VM Slot Capacity"** dashboard shows Apple silicon VM slots per node and
per Orka namespace. Each Apple silicon node advertises its slots as the Kubernetes
resource `apple.com/vm`, and every VM holds one. **0 free slots in a namespace** is
exactly when Orka returns *"The maximum supported number of Apple silicon VMs has been
reached"*, even if CPU and memory are free.

This part **does need Kubernetes access** (the rest of the stack does not). It is off
by default; with it off, nothing changes.

**Enable it (tunnel runs in a container, works anywhere Docker does):**
```bash
mkdir -p secrets
kubectl config view --minify --flatten --context <your-context> > secrets/kubeconfig
chmod 600 secrets/kubeconfig
# in .env:
#   COMPOSE_PROFILES=ksm-tunnel
#   KSM_TARGET=ksm-tunnel:8080
docker compose up -d
```
The `ksm-tunnel` container (official `registry.k8s.io/kubectl`) runs
`kubectl port-forward` to `monitoring/kps-kube-state-metrics:8080` (override with
`KSM_NAMESPACE`, `KSM_SERVICE`, `KSM_PORT`). It only port-forwards; it changes nothing
on the cluster. `secrets/` is gitignored — never commit a kubeconfig.
If kube-state-metrics is already reachable directly, skip the tunnel: leave
`COMPOSE_PROFILES` unset and set `KSM_TARGET=<host>:<port>`.

**Metrics explained**
```
capacity  = kube_node_status_allocatable{resource="apple_com_vm"}
            joined to kube_node_labels (label_orka_macstadium_com_namespace)
in use    = kube_pod_container_resource_requests{resource="apple_com_vm"}
            for Pending/Running pods only (kube_pod_status_phase), scheduled to a node
free      = capacity - in use
waiting   = VM pods with kube_pod_status_scheduled{condition="false"}
```
kube-state-metrics keeps reporting requests for completed/failed pods until they are
deleted, which is why *in use* is filtered by pod phase. A VM also needs free CPU and
memory, so free slots show when a deploy **cannot** succeed, not that it will.

## Optional: Firewall metrics (SNMP)

Polls the Cisco ASA / ASAv firewall in front of the cluster over SNMPv3 and charts it
in Grafana. Off by default; nothing changes unless you enable the `snmp-ssd` profile.
Everything below is parameterised, so clone the repo, fill in `.env`, and it runs
against your own firewall.

### What was built

| Piece | Where | Notes |
|---|---|---|
| snmp_exporter config | [`snmp/snmp.yml`](snmp/snmp.yml) | Hand-written with numeric OIDs, no MIB download or generator run needed. Holds **no credentials**; they are expanded from `.env` at start-up (`--config.expand-environment-variables`). |
| Exporter service | [`docker-compose.yml`](docker-compose.yml) → `snmp-exporter-ssd` (profile `snmp-ssd`) | `prom/snmp-exporter`, reachable inside the compose network as `snmp-exporter-ssd:9116`. |
| Prometheus job | [`prometheus/generate-config.sh`](prometheus/generate-config.sh) → job `macstadium-firewall-ssd` | Rendered only when `FW_SNMP_TARGET` is set. 60 s interval, 30 s timeout, series labelled `firewall="$FW_NAME"`, `site="$SITE"`. |
| Dashboard | [`grafana/dashboards/firewall-ssd.json`](grafana/dashboards/firewall-ssd.json) — **Firewall — Cisco ASA/ASAv (SNMP)** (uid `orka-firewall-ssd`) | Licence utilisation now / P95 7 d / P95 30 d, CPU, memory, connections in use vs peak, new-connection rate, connections declined, IPsec tunnels, remote-access VPN sessions, per-interface throughput / errors / discards / state, uptime, ten ASP drop reasons. Variables: `licence_mbps` (licensed throughput) and `wan_if` (outside interface name). |
| Overview row | [`grafana/dashboards/customer-overview.json`](grafana/dashboards/customer-overview.json) | The same firewall panels sit in a row at the bottom of **Orka — Customer Overview**. |

What the exporter fetches (34 OIDs, all confirmed returning data from an ASAv on 9 October 2026):
`sysUpTime`, CPU 1 min / 5 min, memory pool used / free, connections in use and peak,
per-interface `ifName`, `ifHCInOctets`, `ifHCOutOctets`, `ifHighSpeed`, `ifOperStatus`,
in/out discards and errors, remote-access sessions, IKE and IPsec active tunnels,
connection setup rate 1 min / 5 min, active connections, connections declined for lack
of resources, and ten ASP drop counters (`acl_drop`, `rate_exceeded`, `no_route`,
`nat_no_xlate_to_pat_pool`, `shunned`, `punt_no_mem`, `tcp_not_syn`, `tcp_3whs_failed`,
`tcp_rstfin_ooo`, `interface_down`).

### Step 1 — create a read-only SNMPv3 user on the firewall

Needs administrator access on the ASA. **Add lines only**; never alter or remove
existing `snmp-server` lines, other monitoring may depend on them.

```
snmp-server group <group> v3 priv
snmp-server user <username> <group> v3 auth sha256 <auth-password> priv aes 128 <priv-password>
snmp-server host <interface> <collector-ip> poll version 3 <username>
write memory
```

- `<group>` / `<username>` — names of your choice, e.g. `monitoring-group` / `monitoring`.
- `<interface>` — the firewall `nameif` on which it sees your collector (e.g. `inside`).
- `<collector-ip>` — the address the firewall sees you from. Over a VPN that is your
  VPN-assigned address, not your LAN address.
- Confirm with `show running-config snmp-server` (three new lines) and that
  `write memory` returned `[OK]`.

### Step 2 — fill in `.env`

```
COMPOSE_PROFILES=snmp-ssd            # append to any profile you already use, e.g. ksm-tunnel,snmp-ssd
FW_SNMP_TARGET=<firewall-inside-ip>  # the address you reach the firewall on
FW_NAME=<firewall-name>              # label on every series, e.g. CUSTOMER-FWC01
FW_SNMP_USER=<username>
FW_SNMP_AUTH_PASSWORD=<auth-password>
FW_SNMP_PRIV_PASSWORD=<priv-password>
```

`.env` is gitignored. Keep the passwords out of shell history too (do not paste the
`snmp-server user` line into a terminal that keeps history).

### Step 3 — start and verify

```bash
docker compose up -d

# 1. The exporter can reach the firewall and the firewall answers (expect sysUpTime, ifHCInOctets, ...):
docker compose exec prometheus wget -qO- \
  'http://snmp-exporter-ssd:9116/snmp?auth=ssd_v3&module=cisco_asa&target=<firewall-inside-ip>' | head -20

# 2. Prometheus sees the target as UP:
curl -s localhost:9090/api/v1/targets | grep -o '"job":"macstadium-firewall-ssd"[^}]*"health":"[a-z]*"'

# 3. A series exists:
curl -s --data-urlencode 'query=up{job="macstadium-firewall-ssd"}' localhost:9090/api/v1/query
```

Then open Grafana → **Firewall — Cisco ASA/ASAv (SNMP)** and set `licence_mbps` and
`wan_if` at the top of the dashboard.

### Constraints learned on the way

- Poll no faster than every 5 s (the job uses 60 s). Keep the walk list narrow: never
  walk `1.3.6.1` or `1.3.6.1.4.1.9`, and never walk the ASP drop table (531 rows). The
  ten drop counters are fetched by exact index with a single GET.
- `max_repetitions: 10` keeps GETBULK replies small. The ASA sets Don't Fragment on
  responses, so large replies are lost on small-MTU paths (VPNs included).
- `crasNumTotalFailures` (`...392.1.3.21`) is deliberately absent: on ASAv it returns many
  values under one name and the whole scrape fails with HTTP 500.
- Cisco does not support SNMP polling through a VPN tunnel via the management-access
  feature. If the target never answers from your VPN address, run this stack on a host
  inside the firewall instead.
- Tested on an ASAv in a lab in October 2026. Other models can expose a different
  `cpmCPUTotalIndex` / memory pool layout; the dashboard queries aggregate over them.

## Dashboards and docs

| File | Dashboard | Needs |
|---|---|---|
| `grafana/dashboards/customer-overview.json` | Orka — Customer Overview | operator `:8080` + node exporters `:9100` (firewall row fills when `snmp-ssd` is on) |
| `grafana/dashboards/orka-operator.json` | Orka Operator | operator `:8080` |
| `grafana/dashboards/capacity.json` | Orka — VM Slot Capacity | kube-state-metrics (`ksm-tunnel` profile or direct `KSM_TARGET`) |
| `grafana/dashboards/firewall-ssd.json` | Firewall — Cisco ASA/ASAv (SNMP) | `snmp-ssd` profile |
| `grafana/dashboards/customer-x-example.json` | Orka — Customer X Example (customer-consumable metrics) | operator + node exporters + kube-state-metrics; built only from endpoints documented as customer-scrapable |

- [`docs/customer-x-example-dashboard.md`](docs/customer-x-example-dashboard.md) — panel-by-panel reference for the Customer X example: metric, labels, PromQL, meaning, and what cannot be charted from customer-reachable endpoints.
- [`docs/gen_customer_x_dash.py`](docs/gen_customer_x_dash.py) — generator for that dashboard; edit and re-run `python3 docs/gen_customer_x_dash.py grafana/dashboards/customer-x-example.json`.
- [`docs/orka-metrics-catalogue.md`](docs/orka-metrics-catalogue.md) — every metric family exposed by each customer-reachable Orka component, captured from a lab cluster.

## Notes
- Metrics are scraped from the Orka operator (`:8080`) and node exporters (`:9100`)
- This project does not modify the Orka cluster (the optional `ksm-tunnel` only port-forwards)
- `prometheus/prometheus.yml` is generated (gitignored); edit `.env`, not that file

## References

**MacStadium (public docs)**
- [Consuming Metrics from Prometheus](https://docs.macstadium.com/orka/orka-resources/consuming-metrics-from-prometheus) — the Orka endpoints this stack scrapes, with an example `prometheus.yml`
- [Viewing your environment in My Cloud](https://docs.macstadium.com/macstadium/macstadium-overview/ip-plan) — where the IP Allocation table, Host Assignments and VPN credentials live
- [Connect to your Orka cluster via VPN](https://docs.macstadium.com/orka/networking-with-orka-at-macstadium/vpn-connection) — getting onto the private network from a laptop
- [Logging into Cisco Firewall](https://docs.macstadium.com/iaas/cisco-firewalls/logging-into-cisco-firewall) and [Creating Local User Accounts on a Cisco ASA](https://docs.macstadium.com/iaas/cisco-firewalls/creating-local-user-accounts-on-a-cisco-asa) — admin access needed for the `snmp-server` lines in Step 1 of the firewall section
- [Orka release notes](https://docs.macstadium.com/orka/orka-upgrades-and-release-notes/orka-release-notes) — metric additions per version

**Upstream**
- [prometheus/snmp_exporter](https://github.com/prometheus/snmp_exporter) — `snmp.yml` format, `--config.expand-environment-variables`, the `/snmp?auth=&module=&target=` query
- [Prometheus configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/) — `scrape_configs`, `relabel_configs`
- [Grafana provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/) — how `grafana/provisioning/` loads the dashboards and datasource
- [Cisco ASA SNMP Version 3 Tools Implementation Guide](https://www.cisco.com/c/en/us/td/docs/security/asa/snmp/guide/snmp-version-3-tools-implementation-guide/m-overview.html) — configure group, then user, then host, in that order
