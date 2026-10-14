import json, sys

DS = {"type": "prometheus", "uid": "prometheus"}
panels = []
_id = [0]
y = [0]


def nid():
    _id[0] += 1
    return _id[0]


def thr(*steps):
    return {"mode": "absolute", "steps": [{"color": c, "value": v} for c, v in steps]}


def target(expr, legend="", instant=False, fmt=None):
    t = {"datasource": DS, "expr": expr, "legendFormat": legend, "refId": chr(65 + target.n)}
    target.n += 1
    if instant:
        t["instant"] = True
        t["range"] = False
    if fmt:
        t["format"] = fmt
    return t


target.n = 0


def mk(ptype, title, desc, targets, x, w, h, unit=None, thresholds=None, extra=None, options=None, mn=None, mx=None):
    target.n = 0
    ts = [target(*t) if isinstance(t, tuple) else t for t in targets]
    # re-letter refIds
    for i, t in enumerate(ts):
        t["refId"] = chr(65 + i)
    d = {"id": nid(), "type": ptype, "title": title, "description": desc, "datasource": DS,
         "gridPos": {"x": x, "y": y[0], "w": w, "h": h}, "targets": ts,
         "fieldConfig": {"defaults": {}, "overrides": []}, "options": options or {}}
    f = d["fieldConfig"]["defaults"]
    if unit:
        f["unit"] = unit
    if thresholds:
        f["thresholds"] = thresholds
    if mn is not None:
        f["min"] = mn
    if mx is not None:
        f["max"] = mx
    if extra:
        f.update(extra)
    panels.append(d)
    return d


def row(title):
    y[0] += 0
    panels.append({"id": nid(), "type": "row", "title": title, "collapsed": False,
                   "gridPos": {"x": 0, "y": y[0], "w": 24, "h": 1}, "panels": []})
    y[0] += 1


def text(title, md, x, w, h):
    panels.append({"id": nid(), "type": "text", "title": title, "gridPos": {"x": x, "y": y[0], "w": w, "h": h},
                   "options": {"mode": "markdown", "content": md}})


def end_line(h):
    y[0] += h


STAT = {"reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "colorMode": "background",
        "graphMode": "none", "textMode": "auto", "orientation": "auto"}
BAR = {"reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False}, "orientation": "horizontal",
       "displayMode": "gradient", "showUnfilled": True}
TS = {"legend": {"displayMode": "list", "placement": "bottom", "showLegend": True}, "tooltip": {"mode": "multi"}}

NODE = ' * on (instance) group_left (nodename) node_uname_info'
DATA = '{mountpoint="/System/Volumes/Data",fstype="apfs"}'
NFS = '{fstype="nfs"}'

# ---------------------------------------------------------------- header
text("What this dashboard is",
     "## Customer X example: only customer-consumable Orka metrics\n"
     "Built to show what a customer's **own Prometheus + Grafana** can chart against the Customer X \"service review\" "
     "(Sept 2026) asks **R1, R2, D3 and O3**, using only endpoints documented as customer-scrapable.\n\n"
     "| Job in this stack | Endpoint scraped | Provides |\n|---|---|---|\n"
     "| `orka-operator` | `<orka LB IP>:8080/metrics` | the 10 `orka_operator_*` VM metrics |\n"
     "| `orka-nodes` | `<node IP>:9100/metrics` | node_exporter: filesystem, CPU, memory, load, network |\n"
     "| `kube-state-metrics` | `<orka LB IP>:9101/metrics` (here via a read-only port-forward) | node conditions, pod phases, node capacity |\n\n"
     "Panels whose title ends **(not available)** or the final text panel mark asks that **no endpoint documented as customer-reachable can answer**. "
     "Every panel's description (hover the **i** icon) lists its exact metric, job, labels and PromQL. "
     "Lab source: L20 (ORKL10000020). Full write-up: `docs/customer-x-example-dashboard.md`.",
     0, 24, 6)
end_line(6)

# ---------------------------------------------------------------- R1 / O3 nodes
row("R1 / O3 — Node health  (kube-state-metrics :9101, node_exporter :9100)")
mk("stat", "Nodes Ready",
   "Metric: `kube_node_status_condition` (gauge, 0/1) from job `kube-state-metrics`.\nLabels used: `condition=\"Ready\"`, `status=\"true\"`.\n"
   "PromQL: count of series equal to 1.\nMeaning: Kubernetes' own view of how many nodes (masters included) report Ready. "
   "This is the closest customer-visible signal to ask R1 (node failure detection).",
   [('count(kube_node_status_condition{condition="Ready",status="true"} == 1)', "Ready", True)],
   0, 4, 4, thresholds=thr(("red", None), ("green", 1)), options=STAT)
mk("stat", "Nodes NotReady / Unknown",
   "Metric: `kube_node_status_condition`, job `kube-state-metrics`.\nLabels: `condition=\"Ready\"`, `status=~\"false|unknown\"`.\n"
   "PromQL: count of those series equal to 1, `or vector(0)` so the panel shows 0 instead of 'No data'.\n"
   "Meaning: nodes Kubernetes reports as not Ready or Unknown. Red when above zero.",
   [('count(kube_node_status_condition{condition="Ready",status=~"false|unknown"} == 1) or vector(0)', "Not ready", True)],
   4, 4, 4, thresholds=thr(("green", None), ("red", 1)), options=STAT)
mk("stat", "node_exporter targets down",
   "Metric: `up` (Prometheus' own scrape result), job `orka-nodes`.\nPromQL: `count(up{job=\"orka-nodes\"} == 0) or vector(0)`.\n"
   "Meaning: node exporters this Prometheus cannot scrape. Distinct from Kubernetes readiness: a node can be Ready while its exporter is unreachable, and the reverse.",
   [('count(up{job="orka-nodes"} == 0) or vector(0)', "Down", True)],
   8, 4, 4, thresholds=thr(("green", None), ("red", 1)), options=STAT)
mk("table", "Nodes not Ready (detail)",
   "Metric: `kube_node_status_condition`, job `kube-state-metrics`, `condition=\"Ready\"`, `status!=\"true\"`, value 1. "
   "Instant query shown as a table (columns: node, status). Empty table = every node Ready.",
   [('kube_node_status_condition{condition="Ready",status!="true"} == 1', "", True, "table")],
   12, 12, 4,
   options={"showHeader": True},
   extra={"custom": {"align": "auto"}})
panels[-1]["transformations"] = [
    {"id": "organize", "options": {"excludeByName": {"Time": True, "Value": True, "__name__": True, "job": True,
                                                      "instance": True, "endpoint": True, "service": True,
                                                      "namespace": True, "pod": True, "uid": True, "cluster": True,
                                                      "orka_version": True, "tenant": True, "site": True,
                                                      "container": True, "condition": True, "system_uuid": True}}}]
end_line(4)

mk("bargauge", "CPU usage % — by node",
   "Metric: `node_cpu_seconds_total` (counter) with `mode=\"idle\"`, job `orka-nodes`.\n"
   "PromQL: `100 - avg by (instance)(rate(node_cpu_seconds_total{mode=\"idle\"}[1m])) * 100`, joined to `node_uname_info` on `instance` to show the node name.\n"
   "Meaning: host CPU busy %. Supports O3 (node dashboards).",
   [('(100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100))' + NODE, "{{nodename}}", True)],
   0, 12, 8, unit="percent", thresholds=thr(("green", None), ("yellow", 70), ("red", 90)), options=BAR, mn=0, mx=100)
mk("bargauge", "Load average (1m) — by node",
   "Metric: `node_load1` (gauge), job `orka-nodes`, joined to `node_uname_info` for the node name.",
   [('(avg by (instance) (node_load1))' + NODE, "{{nodename}}", True)],
   12, 12, 8, thresholds=thr(("green", None), ("yellow", 8), ("red", 16)), options=BAR, mn=0)
end_line(8)

# ---------------------------------------------------------------- D3 storage
row("D3 — Storage and thresholds  (node_exporter :9100)")
mk("bargauge", "Host data volume used % — macOS nodes  (80% = Customer X's example threshold)",
   "Metrics: `node_filesystem_size_bytes` and `node_filesystem_avail_bytes` (gauges), job `orka-nodes`.\n"
   "Selector: `mountpoint=\"/System/Volumes/Data\", fstype=\"apfs\"` — the writable APFS data volume on the macOS hosts, where VM disk images and cached images live.\n"
   "PromQL: `100 * (1 - avail / size)`, each side wrapped in `max by (instance)`, joined to `node_uname_info` for the node name.\n"
   "Thresholds: yellow 70, red 80 (Customer X's ask D3 cites 80% as an example). Linux nodes do not have this mountpoint and are excluded.\n"
   "Note: this is host free space. It does NOT show how much space the VMs have been allocated (see final text panel).",
   [('(100 * (1 - max by (instance) (node_filesystem_avail_bytes' + DATA + ') / max by (instance) (node_filesystem_size_bytes' + DATA + ')))' + NODE, "{{nodename}}", True)],
   0, 12, 8, unit="percent", thresholds=thr(("green", None), ("yellow", 70), ("red", 80)), options=BAR, mn=0, mx=100)
mk("bargauge", "Host data volume free GiB — macOS nodes",
   "Metric: `node_filesystem_avail_bytes`, same selector as the panel to the left, divided by 1024^3.\nMeaning: absolute headroom. Red below 50 GiB, yellow below 100 GiB (illustrative values, edit to taste).",
   [('(max by (instance) (node_filesystem_avail_bytes' + DATA + ') / 1024 / 1024 / 1024)' + NODE, "{{nodename}}", True)],
   12, 12, 8, unit="decgbytes", thresholds=thr(("red", None), ("yellow", 50), ("green", 100)), options=BAR, mn=0)
end_line(8)
mk("timeseries", "Host data volume used % over time — macOS nodes",
   "Same query as the bar gauge, as a range query, so the slope towards the 80% line is visible. Source: `node_filesystem_*` on job `orka-nodes`. "
   "History is limited to this Prometheus' retention and uptime.",
   [('100 * (1 - max by (instance) (node_filesystem_avail_bytes' + DATA + ') / max by (instance) (node_filesystem_size_bytes' + DATA + '))' + NODE, "{{nodename}}")],
   0, 12, 8, unit="percent", options=TS, mn=0, mx=100,
   thresholds=thr(("green", None), ("red", 80)),
   extra={"custom": {"thresholdsStyle": {"mode": "line"}}})
mk("bargauge", "NFS image-storage mount used %",
   "Metrics: `node_filesystem_size_bytes`, `node_filesystem_avail_bytes`, job `orka-nodes`, selector `fstype=\"nfs\"` "
   "(`/Users/devadmin/mnt` on macOS nodes, `/var/mnt` on the Linux node that mounts it).\n"
   "PromQL: `100 * (1 - avail/size)` grouped by instance and mountpoint.\n"
   "Meaning: capacity of the shared NFS export used for image storage, as seen from each node. All nodes see the same export, so the values should agree; a node that disagrees is worth checking.",
   [('100 * (1 - max by (instance, mountpoint) (node_filesystem_avail_bytes' + NFS + ') / max by (instance, mountpoint) (node_filesystem_size_bytes' + NFS + '))', "{{instance}} {{mountpoint}}", True)],
   12, 12, 8, unit="percent", thresholds=thr(("green", None), ("yellow", 70), ("red", 80)), options=BAR, mn=0, mx=100)
end_line(8)

# ---------------------------------------------------------------- R2 VMs
row("R2 — VM and deployment health  (orka-operator :8080)")
mk("stat", "VM instances",
   "Metric: `orka_operator_virtual_machine_instances_total` (gauge, unlabelled), job `orka-operator`.\nMeaning: VM instances the operator currently counts.",
   [('sum(orka_operator_virtual_machine_instances_total)', "all", True)], 0, 4, 4, thresholds=thr(("blue", None)), options=STAT)
mk("stat", "Apple silicon VMs",
   "Metric: `orka_operator_apple_silicon_virtual_machine_instances_total` (gauge), job `orka-operator`.",
   [('sum(orka_operator_apple_silicon_virtual_machine_instances_total)', "arm", True)], 4, 4, 4, thresholds=thr(("blue", None)), options=STAT)
mk("stat", "Intel VMs",
   "Metric: `orka_operator_intel_virtual_machine_instances_total` (gauge), job `orka-operator`.",
   [('sum(orka_operator_intel_virtual_machine_instances_total)', "intel", True)], 8, 4, 4, thresholds=thr(("blue", None)), options=STAT)
mk("stat", "Deployments OK / failed in range",
   "Metrics: `orka_operator_virtual_machine_successes_total` and `orka_operator_virtual_machine_failures_total` (counters), job `orka-operator`.\n"
   "PromQL: `sum(increase(<counter>[$__range]))`, i.e. over the time range selected at the top of the dashboard.\nMeaning: deployment outcomes the operator recorded.",
   [('sum(increase(orka_operator_virtual_machine_successes_total[$__range]))', "OK", True),
    ('sum(increase(orka_operator_virtual_machine_failures_total[$__range]))', "Failed", True)],
   12, 6, 4, thresholds=thr(("green", None)), options=STAT)
mk("stat", "VM lifetime errors (counter)",
   "Metric: `orka_operator_virtual_machine_lifetime_errors_total` (counter), job `orka-operator`.\n"
   "Per the Engineering metrics reference, this metric is emitted by the operator and is NOT kept in MacStadium's central store, so it exists only for a customer who scrapes `:8080` directly. "
   "The sources do not say what triggers it, so this panel only displays the value and its growth.",
   [('sum(orka_operator_virtual_machine_lifetime_errors_total)', "errors", True)], 18, 6, 4, thresholds=thr(("green", None), ("yellow", 1)), options=STAT)
end_line(4)
mk("timeseries", "VM instances over time",
   "Same three gauges as the stats above, as range queries (job `orka-operator`).",
   [('sum(orka_operator_virtual_machine_instances_total)', "total"),
    ('sum(orka_operator_apple_silicon_virtual_machine_instances_total)', "apple silicon"),
    ('sum(orka_operator_intel_virtual_machine_instances_total)', "intel")],
   0, 8, 8, options=TS, mn=0)
mk("timeseries", "Deployments per 5 minutes",
   "PromQL: `sum(increase(<successes or failures counter>[5m]))`. Counters: `orka_operator_virtual_machine_successes_total`, `orka_operator_virtual_machine_failures_total`.",
   [('sum(increase(orka_operator_virtual_machine_successes_total[5m]))', "OK"),
    ('sum(increase(orka_operator_virtual_machine_failures_total[5m]))', "failed")],
   8, 8, 8, options=TS, mn=0)
mk("timeseries", "Average deployment duration (s)",
   "Metrics: `orka_operator_virtual_machine_success_deployment_duration_seconds` and `..._failed_deployment_duration_seconds` (histograms), using only the `_sum` and `_count` series.\n"
   "PromQL: `rate(_sum[5m]) / rate(_count[5m])`. The line has gaps in any window with no deployments (0/0).\n"
   "These two series are the part of the histograms MacStadium itself keeps centrally; the `_bucket` series are also emitted at `:8080`.",
   [('sum(rate(orka_operator_virtual_machine_success_deployment_duration_seconds_sum[5m])) / sum(rate(orka_operator_virtual_machine_success_deployment_duration_seconds_count[5m]))', "success"),
    ('sum(rate(orka_operator_virtual_machine_failed_deployment_duration_seconds_sum[5m])) / sum(rate(orka_operator_virtual_machine_failed_deployment_duration_seconds_count[5m]))', "failed")],
   16, 8, 8, unit="s", options=TS, mn=0)
end_line(8)

# ---------------------------------------------------------------- capacity
row("Capacity and pod phase  (kube-state-metrics :9101)")
mk("stat", "VM slots allocatable (apple.com/vm)",
   "Metric: `kube_node_status_allocatable` (gauge) with `resource=\"apple_com_vm\"`, job `kube-state-metrics`.\n"
   "PromQL: `sum(...)` across nodes. Meaning: how many VM slots the nodes advertise to Kubernetes.",
   [('sum(kube_node_status_allocatable{resource="apple_com_vm"})', "slots", True)], 0, 6, 5, thresholds=thr(("blue", None)), options=STAT)
mk("timeseries", "Pods by phase in orka-* namespaces",
   "Metric: `kube_pod_status_phase` (gauge, 0/1), job `kube-state-metrics`, `namespace=~\"orka.*\"`.\n"
   "PromQL: `sum by (phase)(... == 1)`. Meaning: pod counts per Kubernetes phase in the tenant namespaces.\n"
   "This panel reports pod phase only. The sources reviewed do not state that one pod equals one VM, so no VM claim is made here. "
   "Note: MacStadium's central store drops `orka-*` namespaces from this metric; a customer scraping `:9101` directly receives them.",
   [('sum by (phase) (kube_pod_status_phase{namespace=~"orka.*"} == 1)', "{{phase}}")],
   6, 18, 5, options=TS, mn=0)
end_line(5)

# ---------------------------------------------------------------- gaps
text("NOT available from any customer-consumable endpoint (per the sources reviewed)",
     "These parts of the Customer X asks have **no metric** at any endpoint documented as customer-reachable. "
     "They are shown so the dashboard does not imply coverage it does not have.\n\n"
     "| Ask | What would be needed | Status |\n|---|---|---|\n"
     "| D3 / D1 | VM disk **allocated vs physical** (over-commit) | no metric; only host free space exists |\n"
     "| D2 | Image-cache size, cached-image count, stale entries | no metric |\n"
     "| R1 | Orka Engine / agent / WindowServer process health; virtual-kubelet heartbeat | virtual-kubelet exposes no `/metrics`; no Engine or agent metric listed |\n"
     "| R2 | Per-VM health or liveness; per-VM, per-node or per-namespace breakdown | operator metrics are 10 unlabelled series (the `vm_namespace` label is a 3.7.0-alpha addition) |\n"
     "| O3 | Firewall throughput, discards, session counts | not on the cluster; reached only via the MacStadium portal GraphQL API |\n"
     "| O2 | Notification by MacStadium | not a metric; internal alerting exists but customer notification is undocumented |\n\n"
     "Alerting itself (an alert at 80% disk, for example) would be a Prometheus alert rule plus Alertmanager on the customer's side. "
     "This dashboard only draws thresholds; it does not send alerts.",
     0, 24, 9)
end_line(9)

dash = {
    "uid": "orka-customer-x-example",
    "title": "Orka — Customer X Example (customer-consumable metrics)",
    "tags": ["orka", "customer-x-example", "customer-metrics"],
    "timezone": "browser", "schemaVersion": 39, "version": 1, "editable": True, "graphTooltip": 1,
    "refresh": "30s", "time": {"from": "now-3h", "to": "now"},
    "annotations": {"list": []}, "templating": {"list": []}, "panels": panels,
    "description": "Example dashboard built only from customer-scrapable Orka endpoints (operator :8080, kube-state-metrics :9101, node_exporter :9100), mapped to the Customer X review asks R1, R2, D3, O3. Panels marked not available have no customer-consumable metric.",
}
out = sys.argv[1]
json.dump(dash, open(out, "w"), indent=2, ensure_ascii=False)
print("panels:", len(panels), "->", out)
