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
  echo "  scrape_interval: 30s"
  echo "  evaluation_interval: 30s"
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
  echo ""
  echo "  # OCI / Harbor registry — add once the metrics endpoint is known:"
  echo "  # - job_name: oci-registry"
  echo "  #   static_configs:"
  echo "  #     - targets: [\"<harbor-ip>:9107\"]"
} > "$OUT"

echo "generate-config.sh: wrote $OUT for cluster=${CLUSTER_NAME} (orka ${ORKA_VERSION})"
