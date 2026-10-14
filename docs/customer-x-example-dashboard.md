# Customer X example dashboard — customer-consumable Orka metrics

Dashboard: **Orka — Customer X Example (customer-consumable metrics)**, uid `orka-customer-x-example`, Grafana folder `Orka`, file `grafana/dashboards/customer-x-example.json`.

Created 6 October 2026 against lab cluster L20 (ORKL10000020). Purpose: show, with a customer's own Prometheus and Grafana, what can be charted for the Customer X service-review (September 2026) asks R1, R2, D3 and O3, and where nothing can be charted.

## 1. Data flow

```
Orka cluster endpoints (customer-scrapable)          oc-prometheus (laptop, docker compose)         Grafana
  <orka LB IP>:8080/metrics   orka-operator   ──┐
  <node IP>:9100/metrics      node_exporter   ──┼──► Prometheus :9090 (scrape_interval 5s) ──► Grafana :3000
  <orka LB IP>:9101/metrics   kube-state-metrics ┘      datasource uid `prometheus`              folder `Orka`
```

| Prometheus job | Target(s) in this lab | Documented customer endpoint | Metric families used by this dashboard |
|---|---|---|---|
| `orka-operator` | `10.221.192.20:8080` | operator `:8080/metrics` | `orka_operator_*` (10 series) |
| `orka-nodes` | `10.221.192.31–.39:9100` (9 hosts; 8 reporting, .33 down) | node_exporter `:9100/metrics` | `node_filesystem_*`, `node_cpu_seconds_total`, `node_load1`, `node_uname_info`, `up` |
| `kube-state-metrics` | `ksm-tunnel:8080` (read-only `kubectl port-forward` to `monitoring/kps-kube-state-metrics:8080`) | kube-state-metrics `:9101/metrics` on the Orka LB IP | `kube_node_status_condition`, `kube_node_status_allocatable`, `kube_pod_status_phase` |

In a customer's own environment, replace the targets in `prometheus.yml` with the cluster's LoadBalancer IP (`:8080`, `:9101`) and node IPs (`:9100`). The `ksm-tunnel` container exists only because this lab was reached via a kubeconfig; a customer who can reach `:9101` directly does not need it. Reachability of those ports is per cluster (ASA rules) and was not tested for any customer.

## 2. Panel-by-panel reference

Every panel's description inside Grafana carries the same information. Query text below is copied from the dashboard JSON.

### R1 / O3 — Node health  (kube-state-metrics :9101, node_exporter :9100)

**Nodes Ready**  (`stat`)

Metric: `kube_node_status_condition` (gauge, 0/1) from job `kube-state-metrics`.
Labels used: `condition="Ready"`, `status="true"`.
PromQL: count of series equal to 1.
Meaning: Kubernetes' own view of how many nodes (masters included) report Ready. This is the closest customer-visible signal to ask R1 (node failure detection).

- `A` (instant, legend `Ready`): `count(kube_node_status_condition{condition="Ready",status="true"} == 1)`
- Thresholds: red (base), green ≥ 1

**Nodes NotReady / Unknown**  (`stat`)

Metric: `kube_node_status_condition`, job `kube-state-metrics`.
Labels: `condition="Ready"`, `status=~"false|unknown"`.
PromQL: count of those series equal to 1, `or vector(0)` so the panel shows 0 instead of 'No data'.
Meaning: nodes Kubernetes reports as not Ready or Unknown. Red when above zero.

- `A` (instant, legend `Not ready`): `count(kube_node_status_condition{condition="Ready",status=~"false|unknown"} == 1) or vector(0)`
- Thresholds: green (base), red ≥ 1

**node_exporter targets down**  (`stat`)

Metric: `up` (Prometheus' own scrape result), job `orka-nodes`.
PromQL: `count(up{job="orka-nodes"} == 0) or vector(0)`.
Meaning: node exporters this Prometheus cannot scrape. Distinct from Kubernetes readiness: a node can be Ready while its exporter is unreachable, and the reverse.

- `A` (instant, legend `Down`): `count(up{job="orka-nodes"} == 0) or vector(0)`
- Thresholds: green (base), red ≥ 1

**Nodes not Ready (detail)**  (`table`)

Metric: `kube_node_status_condition`, job `kube-state-metrics`, `condition="Ready"`, `status!="true"`, value 1. Instant query shown as a table (columns: node, status). Empty table = every node Ready.

- `A` (instant, legend ``): `kube_node_status_condition{condition="Ready",status!="true"} == 1`

**CPU usage % — by node**  (`bargauge`)

Metric: `node_cpu_seconds_total` (counter) with `mode="idle"`, job `orka-nodes`.
PromQL: `100 - avg by (instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100`, joined to `node_uname_info` on `instance` to show the node name.
Meaning: host CPU busy %. Supports O3 (node dashboards).

- `A` (instant, legend `{{nodename}}`): `(100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)) * on (instance) group_left (nodename) node_uname_info`
- Thresholds: green (base), yellow ≥ 70, red ≥ 90
- Unit: `percent`

**Load average (1m) — by node**  (`bargauge`)

Metric: `node_load1` (gauge), job `orka-nodes`, joined to `node_uname_info` for the node name.

- `A` (instant, legend `{{nodename}}`): `(avg by (instance) (node_load1)) * on (instance) group_left (nodename) node_uname_info`
- Thresholds: green (base), yellow ≥ 8, red ≥ 16

### D3 — Storage and thresholds  (node_exporter :9100)

**Host data volume used % — macOS nodes  (80% = Customer X's example threshold)**  (`bargauge`)

Metrics: `node_filesystem_size_bytes` and `node_filesystem_avail_bytes` (gauges), job `orka-nodes`.
Selector: `mountpoint="/System/Volumes/Data", fstype="apfs"` — the writable APFS data volume on the macOS hosts, where VM disk images and cached images live.
PromQL: `100 * (1 - avail / size)`, each side wrapped in `max by (instance)`, joined to `node_uname_info` for the node name.
Thresholds: yellow 70, red 80 (Customer X's ask D3 cites 80% as an example). Linux nodes do not have this mountpoint and are excluded.
Note: this is host free space. It does NOT show how much space the VMs have been allocated (see final text panel).

- `A` (instant, legend `{{nodename}}`): `(100 * (1 - max by (instance) (node_filesystem_avail_bytes{mountpoint="/System/Volumes/Data",fstype="apfs"}) / max by (instance) (node_filesystem_size_bytes{mountpoint="/System/Volumes/Data",fstype="apfs"}))) * on (instance) group_left (nodename) node_uname_info`
- Thresholds: green (base), yellow ≥ 70, red ≥ 80
- Unit: `percent`

**Host data volume free GiB — macOS nodes**  (`bargauge`)

Metric: `node_filesystem_avail_bytes`, same selector as the panel to the left, divided by 1024^3.
Meaning: absolute headroom. Red below 50 GiB, yellow below 100 GiB (illustrative values, edit to taste).

- `A` (instant, legend `{{nodename}}`): `(max by (instance) (node_filesystem_avail_bytes{mountpoint="/System/Volumes/Data",fstype="apfs"}) / 1024 / 1024 / 1024) * on (instance) group_left (nodename) node_uname_info`
- Thresholds: red (base), yellow ≥ 50, green ≥ 100
- Unit: `decgbytes`

**Host data volume used % over time — macOS nodes**  (`timeseries`)

Same query as the bar gauge, as a range query, so the slope towards the 80% line is visible. Source: `node_filesystem_*` on job `orka-nodes`. History is limited to this Prometheus' retention and uptime.

- `A` (range, legend `{{nodename}}`): `100 * (1 - max by (instance) (node_filesystem_avail_bytes{mountpoint="/System/Volumes/Data",fstype="apfs"}) / max by (instance) (node_filesystem_size_bytes{mountpoint="/System/Volumes/Data",fstype="apfs"})) * on (instance) group_left (nodename) node_uname_info`
- Thresholds: green (base), red ≥ 80
- Unit: `percent`

**NFS image-storage mount used %**  (`bargauge`)

Metrics: `node_filesystem_size_bytes`, `node_filesystem_avail_bytes`, job `orka-nodes`, selector `fstype="nfs"` (`/Users/devadmin/mnt` on macOS nodes, `/var/mnt` on the Linux node that mounts it).
PromQL: `100 * (1 - avail/size)` grouped by instance and mountpoint.
Meaning: capacity of the shared NFS export used for image storage, as seen from each node. All nodes see the same export, so the values should agree; a node that disagrees is worth checking.

- `A` (instant, legend `{{instance}} {{mountpoint}}`): `100 * (1 - max by (instance, mountpoint) (node_filesystem_avail_bytes{fstype="nfs"}) / max by (instance, mountpoint) (node_filesystem_size_bytes{fstype="nfs"}))`
- Thresholds: green (base), yellow ≥ 70, red ≥ 80
- Unit: `percent`

### R2 — VM and deployment health  (orka-operator :8080)

**VM instances**  (`stat`)

Metric: `orka_operator_virtual_machine_instances_total` (gauge, unlabelled), job `orka-operator`.
Meaning: VM instances the operator currently counts.

- `A` (instant, legend `all`): `sum(orka_operator_virtual_machine_instances_total)`
- Thresholds: blue (base)

**Apple silicon VMs**  (`stat`)

Metric: `orka_operator_apple_silicon_virtual_machine_instances_total` (gauge), job `orka-operator`.

- `A` (instant, legend `arm`): `sum(orka_operator_apple_silicon_virtual_machine_instances_total)`
- Thresholds: blue (base)

**Intel VMs**  (`stat`)

Metric: `orka_operator_intel_virtual_machine_instances_total` (gauge), job `orka-operator`.

- `A` (instant, legend `intel`): `sum(orka_operator_intel_virtual_machine_instances_total)`
- Thresholds: blue (base)

**Deployments OK / failed in range**  (`stat`)

Metrics: `orka_operator_virtual_machine_successes_total` and `orka_operator_virtual_machine_failures_total` (counters), job `orka-operator`.
PromQL: `sum(increase(<counter>[$__range]))`, i.e. over the time range selected at the top of the dashboard.
Meaning: deployment outcomes the operator recorded.

- `A` (instant, legend `OK`): `sum(increase(orka_operator_virtual_machine_successes_total[$__range]))`
- `B` (instant, legend `Failed`): `sum(increase(orka_operator_virtual_machine_failures_total[$__range]))`
- Thresholds: green (base)

**VM lifetime errors (counter)**  (`stat`)

Metric: `orka_operator_virtual_machine_lifetime_errors_total` (counter), job `orka-operator`.
Per the Engineering metrics reference, this metric is emitted by the operator and is NOT kept in MacStadium's central store, so it exists only for a customer who scrapes `:8080` directly. The sources do not say what triggers it, so this panel only displays the value and its growth.

- `A` (instant, legend `errors`): `sum(orka_operator_virtual_machine_lifetime_errors_total)`
- Thresholds: green (base), yellow ≥ 1

**VM instances over time**  (`timeseries`)

Same three gauges as the stats above, as range queries (job `orka-operator`).

- `A` (range, legend `total`): `sum(orka_operator_virtual_machine_instances_total)`
- `B` (range, legend `apple silicon`): `sum(orka_operator_apple_silicon_virtual_machine_instances_total)`
- `C` (range, legend `intel`): `sum(orka_operator_intel_virtual_machine_instances_total)`

**Deployments per 5 minutes**  (`timeseries`)

PromQL: `sum(increase(<successes or failures counter>[5m]))`. Counters: `orka_operator_virtual_machine_successes_total`, `orka_operator_virtual_machine_failures_total`.

- `A` (range, legend `OK`): `sum(increase(orka_operator_virtual_machine_successes_total[5m]))`
- `B` (range, legend `failed`): `sum(increase(orka_operator_virtual_machine_failures_total[5m]))`

**Average deployment duration (s)**  (`timeseries`)

Metrics: `orka_operator_virtual_machine_success_deployment_duration_seconds` and `..._failed_deployment_duration_seconds` (histograms), using only the `_sum` and `_count` series.
PromQL: `rate(_sum[5m]) / rate(_count[5m])`. The line has gaps in any window with no deployments (0/0).
These two series are the part of the histograms MacStadium itself keeps centrally; the `_bucket` series are also emitted at `:8080`.

- `A` (range, legend `success`): `sum(rate(orka_operator_virtual_machine_success_deployment_duration_seconds_sum[5m])) / sum(rate(orka_operator_virtual_machine_success_deployment_duration_seconds_count[5m]))`
- `B` (range, legend `failed`): `sum(rate(orka_operator_virtual_machine_failed_deployment_duration_seconds_sum[5m])) / sum(rate(orka_operator_virtual_machine_failed_deployment_duration_seconds_count[5m]))`
- Unit: `s`

### Capacity and pod phase  (kube-state-metrics :9101)

**VM slots allocatable (apple.com/vm)**  (`stat`)

Metric: `kube_node_status_allocatable` (gauge) with `resource="apple_com_vm"`, job `kube-state-metrics`.
PromQL: `sum(...)` across nodes. Meaning: how many VM slots the nodes advertise to Kubernetes.

- `A` (instant, legend `slots`): `sum(kube_node_status_allocatable{resource="apple_com_vm"})`
- Thresholds: blue (base)

**Pods by phase in orka-* namespaces**  (`timeseries`)

Metric: `kube_pod_status_phase` (gauge, 0/1), job `kube-state-metrics`, `namespace=~"orka.*"`.
PromQL: `sum by (phase)(... == 1)`. Meaning: pod counts per Kubernetes phase in the tenant namespaces.
This panel reports pod phase only. The sources reviewed do not state that one pod equals one VM, so no VM claim is made here. Note: MacStadium's central store drops `orka-*` namespaces from this metric; a customer scraping `:9101` directly receives them.

- `A` (range, legend `{{phase}}`): `sum by (phase) (kube_pod_status_phase{namespace=~"orka.*"} == 1)`

**NOT available from any customer-consumable endpoint (per the sources reviewed)**  (`text`)

Text panel; content is shown on the dashboard.

## 3. How the dashboard is built

1. **Select only series that exist.** Each metric was confirmed in this Prometheus (`count(<metric>)`) and each label value was read from live series (for example `mountpoint="/System/Volumes/Data"`, `fstype="apfs"` on macOS hosts; `fstype="nfs"` for the image export; `condition="Ready"`, `status` of `true`/`false`/`unknown`; `resource="apple_com_vm"`).
2. **Join to a node name.** node_exporter series carry `instance` (IP:9100). `node_uname_info` (value 1) carries `nodename`; multiplying by it with `* on (instance) group_left (nodename) node_uname_info` adds the host name without changing values. Filesystem series are first reduced with `max by (instance)` so the join is one-to-one.
3. **Write PromQL per panel**: gauges are read directly; counters use `increase()` or `rate()`; histograms use only `_sum` and `_count`; boolean-style gauges (`kube_node_status_condition`, `kube_pod_status_phase`) are filtered with `== 1` and counted.
4. **Generate the JSON.** `docs/gen_customer_x_dash.py` builds the dashboard (schemaVersion 39) from helper functions (`mk`, `row`, `text`) and writes `grafana/dashboards/customer-x-example.json`. Edit the script and re-run: `python3 docs/gen_customer_x_dash.py grafana/dashboards/customer-x-example.json`.
5. **Provisioning.** `grafana/provisioning/dashboards/dashboards.yml` loads every `*.json` in `/var/lib/grafana/dashboards` (mounted from `grafana/dashboards`) into the `Orka` folder, so the file is picked up within seconds with no Grafana restart. The datasource is `Prometheus` (uid `prometheus`, `http://prometheus:9090`).
6. **Validate.** Every panel query was executed against `localhost:9090` after generation; all 26 panels' queries returned without error.

## 4. Result of the check on 6 October 2026 (L20, read about 11:00Z)

These are readings, not conclusions about any customer.

- 11 nodes report Ready and 1 reports Unknown (x86-mini-3). The node exporter on `10.221.192.33` does not answer.
- Host data volume used on the five macOS hosts is between 30.6% and 96.5% (m2-mini-008 96.5, m2-mini-009 92.4, arm-mini-006 90.9, arm-studio-007 36.3, arm-mini-005 30.6); three of the five read above 90% at the time of the check.
- The NFS export `172.16.174.1:/ORKA-V-LAB-20` reports 0 bytes available of about 1.36 TB on every node that mounts it, so the NFS panel reads 100%.
- Operator: 8 VM instances (7 Apple silicon, 1 Intel); `orka_operator_virtual_machine_lifetime_errors_total` = 28. No deployments occurred in the 3-hour window, so the average-duration lines are empty (0/0).
- Pod phase in `orka-*` namespaces: 6 Running, 2 Pending.

## 5. What this dashboard cannot show

See the final text panel. In short: VM disk over-commit, image-cache contents, Engine/agent/WindowServer health, virtual-kubelet heartbeat, per-VM health, per-namespace breakdown, firewall metrics, and customer notification have no endpoint documented as customer-consumable. Alerting is a customer-side Prometheus alert rule plus Alertmanager; the dashboard draws thresholds only.

## 6. Caveats

- `prometheus/prometheus.yml` is generated from `.env` and labels this lab `orka_version: "3.6.4"`. A Mimir read on 6 October 2026 shows L20's `orka-apiserver` image as `orka-apiserver-dev:3.6.3-latest`. The Customer X dashboard does not use that label.
- Per the Orka release notes, 3.6.0 to 3.6.4 contain no metrics changes, and the dashboard uses only series present in all of them. The 3.7.0-alpha additions (pending-VM queue depth, `vm_namespace` label) are not used.
- The L20 cluster Prometheus runs in agent mode and rejects queries on `:9090` (HTTP 422). That is why this stack scrapes the exporters directly instead of querying the cluster Prometheus.
- The blackbox-exporter (`:9115`) is documented as customer-scrapable but is not scraped by this stack, so no probe panel exists.
- Sources: Orka docs "Consuming metrics from Prometheus"; Orka release notes; an internal MacStadium metrics reference; the Customer X service-review document (September 2026). Live probes of L20 on 6 October 2026.
