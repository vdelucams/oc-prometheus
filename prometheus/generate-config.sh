#!/bin/sh
# Generates prometheus.yml from environment variables (see .env / env.example).
# Run automatically by the "config-init" service in docker-compose.yml so that
# the IP plan lives in ONE place (.env) — Prometheus can't read env vars itself.
set -eu

OUT="${1:-/etc/prometheus/prometheus.yml}"

: "${ORKA_ENDPOINT:?ORKA_ENDPOINT not set (see .env)}"
: "${ORKA_NODE_EXPORTERS:?ORKA_NODE_EXPORTERS not set (see .env)}"
CLUSTER_NAME="${CLUSTER_NAME:-orka}"
ORKA_VERSION="${ORKA_VERSION:-unknown}"
TENANT="${TENANT:-unknown}"
SITE="${SITE:-unknown}"
SCRAPE_INTERVAL="${SCRAPE_INTERVAL:-30s}"
# Optional: kube-state-metrics (host:port). Leave unset for the default,
# no-Kubernetes-access setup. With the ksm-tunnel profile use "ksm-tunnel:8080".
KSM_TARGET="${KSM_TARGET:-}"
# Optional: firewall SNMP polling via the snmp-exporter-ssd service (profile
# "snmp-ssd"). FW_SNMP_TARGET is the firewall's inside IP; leave unset to disable.
FW_SNMP_TARGET="${FW_SNMP_TARGET:-}"
FW_NAME="${FW_NAME:-firewall}"

emit_labels() {
  echo "        labels:"
  echo "          cluster: \"${CLUSTER_NAME}\""
  echo "          orka_version: \"${ORKA_VERSION}\""
  echo "          tenant: \"${TENANT}\""
  echo "          site: \"${SITE}\""
}

{
  echo "# GENERATED from .env by generate-config.sh — do not edit by hand."
  echo "global:"
  echo "  scrape_interval: ${SCRAPE_INTERVAL}"
  echo "  evaluation_interval: ${SCRAPE_INTERVAL}"
  echo ""
  echo "scrape_configs:"
  echo "  - job_name: prometheus"
  echo "    static_configs:"
  echo "      - targets: [\"localhost:9090\"]"
  echo ""
  echo "  - job_name: orka-operator"
  echo "    metrics_path: /metrics"
  echo "    static_configs:"
  echo "      - targets: [\"${ORKA_ENDPOINT}:8080\"]"
  emit_labels
  echo ""
  echo "  - job_name: orka-nodes"
  echo "    metrics_path: /metrics"
  echo "    static_configs:"
  echo "      - targets:"
  OLDIFS="$IFS"; IFS=','
  for t in $ORKA_NODE_EXPORTERS; do
    t="$(echo "$t" | tr -d ' ')"
    [ -n "$t" ] && echo "          - \"$t\""
  done
  IFS="$OLDIFS"
  emit_labels
  if [ -n "$KSM_TARGET" ]; then
    echo ""
    echo "  # kube-state-metrics — VM slot capacity (apple_com_vm) per node/namespace."
    echo "  # honor_labels keeps the exported pod/node/namespace labels as-is."
    echo "  - job_name: kube-state-metrics"
    echo "    metrics_path: /metrics"
    echo "    honor_labels: true"
    echo "    static_configs:"
    echo "      - targets: [\"${KSM_TARGET}\"]"
    emit_labels
  fi
  if [ -n "$FW_SNMP_TARGET" ]; then
    echo ""
    echo "  # Cisco ASA/ASAv firewall via snmp-exporter-ssd. 60s interval / 30s timeout"
    echo "  # follow the polling guidance (never faster than 5s, keep requests narrow)."
    echo "  - job_name: macstadium-firewall-ssd"
    echo "    scrape_interval: 60s"
    echo "    scrape_timeout: 30s"
    echo "    metrics_path: /snmp"
    echo "    params:"
    echo "      auth: [ssd_v3]"
    echo "      module: [cisco_asa]"
    echo "    static_configs:"
    echo "      - targets: [\"${FW_SNMP_TARGET}\"]"
    echo "        labels:"
    echo "          firewall: \"${FW_NAME}\""
    echo "          site: \"${SITE}\""
    echo "    relabel_configs:"
    echo "      - source_labels: [__address__]"
    echo "        target_label: __param_target"
    echo "      - source_labels: [__param_target]"
    echo "        target_label: instance"
    echo "      - target_label: __address__"
    echo "        replacement: snmp-exporter-ssd:9116"
  fi
  echo ""
  echo "  # OCI / Harbor registry — add once the metrics endpoint is known:"
  echo "  # - job_name: oci-registry"
  echo "  #   static_configs:"
  echo "  #     - targets: [\"<harbor-ip>:9107\"]"
} > "$OUT"

echo "generate-config.sh: wrote $OUT for cluster=${CLUSTER_NAME} (orka ${ORKA_VERSION}, scrape ${SCRAPE_INTERVAL}, ksm=${KSM_TARGET:-off})"
