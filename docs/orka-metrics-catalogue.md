# Orka metrics catalogue — every family exposed by each customer-reachable component

Captured **6 October 2026** from lab L20 (ORKL10000020; `orka-apiserver-dev:3.6.3-latest`) with read-only `curl` from a laptop on the labs VPN. Counts are what that cluster emitted at that moment; another cluster or version can differ (for example Linux nodes expose different families from macOS nodes, and probe or per-namespace series appear only when there is something to report). Reachability for a customer depends on the cluster's ASA rules and was not tested.

## Orka operator

Endpoint: `http://<orka LB IP>:8080/metrics`

Documented customer endpoint (PodMonitor `orka-operator`). Orka business metrics plus controller-runtime and Go/process metrics.

**64 metric families, 898 series** in this capture.

| Family | Type | Series | Label keys | Help |
|---|---|---|---|---|
| `certwatcher_read_certificate_errors_total` | counter | 1 | — | Total number of certificate read errors |
| `certwatcher_read_certificate_total` | counter | 1 | — | Total number of certificate reads |
| `controller_runtime_active_workers` | gauge | 10 | controller | Number of currently used workers per controller |
| `controller_runtime_max_concurrent_reconciles` | gauge | 10 | controller | Maximum number of concurrent reconciles per controller |
| `controller_runtime_reconcile_errors_total` | counter | 10 | controller | Total number of reconciliation errors per controller |
| `controller_runtime_reconcile_time_seconds` | histogram | 430 | controller, le | Length of time per reconciliation per controller |
| `controller_runtime_reconcile_total` | counter | 40 | controller, result | Total number of reconciliations per controller |
| `go_gc_duration_seconds` | summary | 7 | quantile | A summary of the wall-time pause (stop-the-world) duration in garbage collection cycles. |
| `go_gc_gogc_percent` | gauge | 1 | — | Heap size target percentage configured by the user, otherwise 100. This value is set by the GOGC environment variable, and the runtime/debug |
| `go_gc_gomemlimit_bytes` | gauge | 1 | — | Go runtime memory limit configured by the user, otherwise math.MaxInt64. This value is set by the GOMEMLIMIT environment variable, and the r |
| `go_goroutines` | gauge | 1 | — | Number of goroutines that currently exist. |
| `go_info` | gauge | 1 | version | Information about the Go environment. |
| `go_memstats_alloc_bytes` | gauge | 1 | — | Number of bytes allocated in heap and currently in use. Equals to /memory/classes/heap/objects:bytes. |
| `go_memstats_alloc_bytes_total` | counter | 1 | — | Total number of bytes allocated in heap until now, even if released already. Equals to /gc/heap/allocs:bytes. |
| `go_memstats_buck_hash_sys_bytes` | gauge | 1 | — | Number of bytes used by the profiling bucket hash table. Equals to /memory/classes/profiling/buckets:bytes. |
| `go_memstats_frees_total` | counter | 1 | — | Total number of heap objects frees. Equals to /gc/heap/frees:objects + /gc/heap/tiny/allocs:objects. |
| `go_memstats_gc_sys_bytes` | gauge | 1 | — | Number of bytes used for garbage collection system metadata. Equals to /memory/classes/metadata/other:bytes. |
| `go_memstats_heap_alloc_bytes` | gauge | 1 | — | Number of heap bytes allocated and currently in use, same as go_memstats_alloc_bytes. Equals to /memory/classes/heap/objects:bytes. |
| `go_memstats_heap_idle_bytes` | gauge | 1 | — | Number of heap bytes waiting to be used. Equals to /memory/classes/heap/released:bytes + /memory/classes/heap/free:bytes. |
| `go_memstats_heap_inuse_bytes` | gauge | 1 | — | Number of heap bytes that are in use. Equals to /memory/classes/heap/objects:bytes + /memory/classes/heap/unused:bytes |
| `go_memstats_heap_objects` | gauge | 1 | — | Number of currently allocated objects. Equals to /gc/heap/objects:objects. |
| `go_memstats_heap_released_bytes` | gauge | 1 | — | Number of heap bytes released to OS. Equals to /memory/classes/heap/released:bytes. |
| `go_memstats_heap_sys_bytes` | gauge | 1 | — | Number of heap bytes obtained from system. Equals to /memory/classes/heap/objects:bytes + /memory/classes/heap/unused:bytes + /memory/classe |
| `go_memstats_last_gc_time_seconds` | gauge | 1 | — | Number of seconds since 1970 of last garbage collection. |
| `go_memstats_mallocs_total` | counter | 1 | — | Total number of heap objects allocated, both live and gc-ed. Semantically a counter version for go_memstats_heap_objects gauge. Equals to /g |
| `go_memstats_mcache_inuse_bytes` | gauge | 1 | — | Number of bytes in use by mcache structures. Equals to /memory/classes/metadata/mcache/inuse:bytes. |
| `go_memstats_mcache_sys_bytes` | gauge | 1 | — | Number of bytes used for mcache structures obtained from system. Equals to /memory/classes/metadata/mcache/inuse:bytes + /memory/classes/met |
| `go_memstats_mspan_inuse_bytes` | gauge | 1 | — | Number of bytes in use by mspan structures. Equals to /memory/classes/metadata/mspan/inuse:bytes. |
| `go_memstats_mspan_sys_bytes` | gauge | 1 | — | Number of bytes used for mspan structures obtained from system. Equals to /memory/classes/metadata/mspan/inuse:bytes + /memory/classes/metad |
| `go_memstats_next_gc_bytes` | gauge | 1 | — | Number of heap bytes when next garbage collection will take place. Equals to /gc/heap/goal:bytes. |
| `go_memstats_other_sys_bytes` | gauge | 1 | — | Number of bytes used for other system allocations. Equals to /memory/classes/other:bytes. |
| `go_memstats_stack_inuse_bytes` | gauge | 1 | — | Number of bytes obtained from system for stack allocator in non-CGO environments. Equals to /memory/classes/heap/stacks:bytes. |
| `go_memstats_stack_sys_bytes` | gauge | 1 | — | Number of bytes obtained from system for stack allocator. Equals to /memory/classes/heap/stacks:bytes + /memory/classes/os-stacks:bytes. |
| `go_memstats_sys_bytes` | gauge | 1 | — | Number of bytes obtained from system. Equals to /memory/classes/total:byte. |
| `go_sched_gomaxprocs_threads` | gauge | 1 | — | The current runtime.GOMAXPROCS setting, or the number of operating system threads that can execute user-level Go code simultaneously. Source |
| `go_threads` | gauge | 1 | — | Number of OS threads created. |
| `leader_election_master_status` | gauge | 1 | name | Gauge of if the reporting system is master of the relevant lease, 0 indicates backup, 1 indicates master. 'name' is the string used to ident |
| `orka_operator_apple_silicon_virtual_machine_instances_total` | gauge | 1 | — | The total number of apple silicon virtual machine instances |
| `orka_operator_intel_virtual_machine_instances_total` | gauge | 1 | — | The total number of intel virtual machine instances |
| `orka_operator_virtual_machine_failed_deployment_duration_seconds` | histogram | 5 | le | The duration of a failed virtual machine deployment |
| `orka_operator_virtual_machine_failures_total` | counter | 1 | — | The total number of virtual machines failures |
| `orka_operator_virtual_machine_instances_total` | gauge | 1 | — | The total number of virtual machine instances |
| `orka_operator_virtual_machine_lifetime_errors_total` | counter | 1 | — | Total number of errors encountered when computing VM lifetime |
| `orka_operator_virtual_machine_lifetime_seconds` | histogram | 15 | le | VM lifecycle duration in seconds (observed on failure or deletion) |
| `orka_operator_virtual_machine_success_deployment_duration_seconds` | histogram | 5 | le | The duration of a successful virtual machine deployment |
| `orka_operator_virtual_machine_successes_total` | counter | 1 | — | The total number of successful virtual machines |
| `orka_operator_virtual_machines_total` | gauge | 1 | — | The total number of virtual machines (pods) |
| `process_cpu_seconds_total` | counter | 1 | — | Total user and system CPU time spent in seconds. |
| `process_max_fds` | gauge | 1 | — | Maximum number of open file descriptors. |
| `process_network_receive_bytes_total` | counter | 1 | — | Number of bytes received by the process over the network. |
| `process_network_transmit_bytes_total` | counter | 1 | — | Number of bytes sent by the process over the network. |
| `process_open_fds` | gauge | 1 | — | Number of open file descriptors. |
| `process_resident_memory_bytes` | gauge | 1 | — | Resident memory size in bytes. |
| `process_start_time_seconds` | gauge | 1 | — | Start time of the process since unix epoch in seconds. |
| `process_virtual_memory_bytes` | gauge | 1 | — | Virtual memory size in bytes. |
| `process_virtual_memory_max_bytes` | gauge | 1 | — | Maximum amount of virtual memory available in bytes. |
| `rest_client_requests_total` | counter | 9 | code, host, method | Number of HTTP requests, partitioned by status code, method, and host. |
| `workqueue_adds_total` | counter | 10 | name | Total number of adds handled by workqueue |
| `workqueue_depth` | gauge | 10 | name | Current depth of workqueue |
| `workqueue_longest_running_processor_seconds` | gauge | 10 | name | How many seconds has the longest running processor for workqueue been running. |
| `workqueue_queue_duration_seconds` | histogram | 130 | le, name | How long in seconds an item stays in workqueue before being requested |
| `workqueue_retries_total` | counter | 10 | name | Total number of retries handled by workqueue |
| `workqueue_unfinished_work_seconds` | gauge | 10 | name | How many seconds of work has been done that is in progress and hasn't been observed by work_duration. Large values indicate stuck threads. O |
| `workqueue_work_duration_seconds` | histogram | 130 | le, name | How long in seconds processing an item from workqueue takes. |

Example raw lines:

```
# TYPE go_goroutines gauge
go_goroutines 223
# TYPE orka_operator_apple_silicon_virtual_machine_instances_total gauge
orka_operator_apple_silicon_virtual_machine_instances_total 7
# TYPE orka_operator_intel_virtual_machine_instances_total gauge
orka_operator_intel_virtual_machine_instances_total 1
# TYPE orka_operator_virtual_machine_failed_deployment_duration_seconds histogram
orka_operator_virtual_machine_failed_deployment_duration_seconds_bucket{le="10"} 25
# TYPE orka_operator_virtual_machine_failures_total counter
orka_operator_virtual_machine_failures_total 30
# TYPE orka_operator_virtual_machine_instances_total gauge
orka_operator_virtual_machine_instances_total 8
# TYPE orka_operator_virtual_machine_lifetime_errors_total counter
orka_operator_virtual_machine_lifetime_errors_total 28
# TYPE orka_operator_virtual_machine_lifetime_seconds histogram
orka_operator_virtual_machine_lifetime_seconds_bucket{le="60"} 129
# TYPE orka_operator_virtual_machine_success_deployment_duration_seconds histogram
orka_operator_virtual_machine_success_deployment_duration_seconds_bucket{le="10"} 28
# TYPE orka_operator_virtual_machine_successes_total counter
orka_operator_virtual_machine_successes_total 185
# TYPE orka_operator_virtual_machines_total gauge
orka_operator_virtual_machines_total 185
```

## kube-state-metrics

Endpoint: `http://<orka LB IP>:9101/metrics`

Documented customer endpoint (svc `kube-state-metrics-lb`). Kubernetes object state: nodes, pods, containers, deployments, jobs, volumes. This is the pod-level source.

**149 metric families, 5437 series** in this capture.

| Family | Type | Series | Label keys | Help |
|---|---|---|---|---|
| `kube_configmap_created` | gauge | 42 | configmap, namespace | [STABLE] Unix creation timestamp |
| `kube_configmap_info` | gauge | 42 | configmap, namespace | [STABLE] Information about configmap. |
| `kube_configmap_metadata_resource_version` | gauge | 42 | configmap, namespace | Resource version representing a specific version of the configmap. |
| `kube_cronjob_created` | gauge | 3 | cronjob, namespace | [STABLE] Unix creation timestamp |
| `kube_cronjob_info` | gauge | 3 | concurrency_policy, cronjob, namespace, schedule | [STABLE] Info about cronjob. |
| `kube_cronjob_metadata_resource_version` | gauge | 3 | cronjob, namespace | [STABLE] Resource version representing a specific version of the cronjob. |
| `kube_cronjob_next_schedule_time` | gauge | 3 | cronjob, namespace | [STABLE] Next time the cronjob should be scheduled. The time after lastScheduleTime, or after the cron job's creation time if it's never bee |
| `kube_cronjob_spec_failed_job_history_limit` | gauge | 3 | cronjob, namespace | Failed job history limit tells the controller how many failed jobs should be preserved. |
| `kube_cronjob_spec_successful_job_history_limit` | gauge | 3 | cronjob, namespace | Successful job history limit tells the controller how many completed jobs should be preserved. |
| `kube_cronjob_spec_suspend` | gauge | 3 | cronjob, namespace | [STABLE] Suspend flag tells the controller to suspend subsequent executions. |
| `kube_cronjob_status_active` | gauge | 3 | cronjob, namespace | [STABLE] Active holds pointers to currently running jobs. |
| `kube_cronjob_status_last_schedule_time` | gauge | 3 | cronjob, namespace | [STABLE] LastScheduleTime keeps information of when was the last time the job was successfully scheduled. |
| `kube_cronjob_status_last_successful_time` | gauge | 3 | cronjob, namespace | LastSuccessfulTime keeps information of when was the last time the job was completed successfully. |
| `kube_daemonset_created` | gauge | 5 | daemonset, namespace | [STABLE] Unix creation timestamp |
| `kube_daemonset_metadata_generation` | gauge | 5 | daemonset, namespace | [STABLE] Sequence number representing a specific generation of the desired state. |
| `kube_daemonset_status_current_number_scheduled` | gauge | 5 | daemonset, namespace | [STABLE] The number of nodes running at least one daemon pod and are supposed to. |
| `kube_daemonset_status_desired_number_scheduled` | gauge | 5 | daemonset, namespace | [STABLE] The number of nodes that should be running the daemon pod. |
| `kube_daemonset_status_number_available` | gauge | 5 | daemonset, namespace | [STABLE] The number of nodes that should be running the daemon pod and have one or more of the daemon pod running and available |
| `kube_daemonset_status_number_misscheduled` | gauge | 5 | daemonset, namespace | [STABLE] The number of nodes running a daemon pod but are not supposed to. |
| `kube_daemonset_status_number_ready` | gauge | 5 | daemonset, namespace | [STABLE] The number of nodes that should be running the daemon pod and have one or more of the daemon pod running and ready. |
| `kube_daemonset_status_number_unavailable` | gauge | 5 | daemonset, namespace | [STABLE] The number of nodes that should be running the daemon pod and have none of the daemon pod running and available |
| `kube_daemonset_status_observed_generation` | gauge | 5 | daemonset, namespace | [STABLE] The most recent generation observed by the daemon set controller. |
| `kube_daemonset_status_updated_number_scheduled` | gauge | 5 | daemonset, namespace | [STABLE] The total number of nodes that are running updated daemon pod |
| `kube_deployment_created` | gauge | 15 | deployment, namespace | [STABLE] Unix creation timestamp |
| `kube_deployment_metadata_generation` | gauge | 15 | deployment, namespace | [STABLE] Sequence number representing a specific generation of the desired state. |
| `kube_deployment_spec_paused` | gauge | 15 | deployment, namespace | [STABLE] Whether the deployment is paused and will not be processed by the deployment controller. |
| `kube_deployment_spec_replicas` | gauge | 15 | deployment, namespace | [STABLE] Number of desired pods for a deployment. |
| `kube_deployment_spec_strategy_rollingupdate_max_surge` | gauge | 14 | deployment, namespace | [STABLE] Maximum number of replicas that can be scheduled above the desired number of replicas during a rolling update of a deployment. |
| `kube_deployment_spec_strategy_rollingupdate_max_unavailable` | gauge | 14 | deployment, namespace | [STABLE] Maximum number of unavailable replicas during a rolling update of a deployment. |
| `kube_deployment_status_condition` | gauge | 90 | condition, deployment, namespace, status | [STABLE] The current status conditions of a deployment. |
| `kube_deployment_status_observed_generation` | gauge | 15 | deployment, namespace | [STABLE] The generation observed by the deployment controller. |
| `kube_deployment_status_replicas` | gauge | 15 | deployment, namespace | [STABLE] The number of replicas per deployment. |
| `kube_deployment_status_replicas_available` | gauge | 15 | deployment, namespace | [STABLE] The number of available replicas per deployment. |
| `kube_deployment_status_replicas_ready` | gauge | 15 | deployment, namespace | [STABLE] The number of ready replicas per deployment. |
| `kube_deployment_status_replicas_unavailable` | gauge | 15 | deployment, namespace | [STABLE] The number of unavailable replicas per deployment. |
| `kube_deployment_status_replicas_updated` | gauge | 15 | deployment, namespace | [STABLE] The number of updated replicas per deployment. |
| `kube_endpoint_address` | gauge | 59 | endpoint, ip, namespace, ready | [STABLE] Information about Endpoint available and non available addresses. |
| `kube_endpoint_address_available` | gauge | 30 | endpoint, namespace | (Deprecated since v2.6.0) Number of addresses available in endpoint. |
| `kube_endpoint_address_not_ready` | gauge | 30 | endpoint, namespace | (Deprecated since v2.6.0) Number of addresses not ready in endpoint |
| `kube_endpoint_created` | gauge | 30 | endpoint, namespace | [STABLE] Unix creation timestamp |
| `kube_endpoint_info` | gauge | 30 | endpoint, namespace | [STABLE] Information about endpoint. |
| `kube_endpoint_ports` | gauge | 35 | endpoint, namespace, port_name, port_number, port_protocol | [STABLE] Information about the Endpoint ports. |
| `kube_job_complete` | gauge | 9 | condition, job_name, namespace | [STABLE] The job has completed its execution. |
| `kube_job_created` | gauge | 3 | job_name, namespace | [STABLE] Unix creation timestamp |
| `kube_job_info` | gauge | 3 | job_name, namespace | [STABLE] Information about job. |
| `kube_job_owner` | gauge | 3 | job_name, namespace, owner_is_controller, owner_kind, owner_name | [STABLE] Information about the Job's owner. |
| `kube_job_spec_completions` | gauge | 3 | job_name, namespace | [STABLE] The desired number of successfully finished pods the job should be run with. |
| `kube_job_spec_parallelism` | gauge | 3 | job_name, namespace | [STABLE] The maximum desired number of pods the job should run at any given time. |
| `kube_job_status_active` | gauge | 3 | job_name, namespace | [STABLE] The number of actively running pods. |
| `kube_job_status_completion_time` | gauge | 3 | job_name, namespace | [STABLE] CompletionTime represents time when the job was completed. |
| `kube_job_status_failed` | gauge | 3 | job_name, namespace | [STABLE] The number of pods which reached Phase Failed and the reason for failure. |
| `kube_job_status_start_time` | gauge | 3 | job_name, namespace | [STABLE] StartTime represents time when the job was acknowledged by the Job Manager. |
| `kube_job_status_succeeded` | gauge | 3 | job_name, namespace | [STABLE] The number of pods which reached Phase Succeeded. |
| `kube_lease_owner` | gauge | 26 | lease, lease_holder, namespace, owner_kind, owner_name | Information about the Lease's owner. |
| `kube_lease_renew_time` | gauge | 26 | lease, namespace | Kube lease renew time. |
| `kube_mutatingwebhookconfiguration_created` | gauge | 12 | mutatingwebhookconfiguration, namespace | Unix creation timestamp. |
| `kube_mutatingwebhookconfiguration_info` | gauge | 12 | mutatingwebhookconfiguration, namespace | Information about the MutatingWebhookConfiguration. |
| `kube_mutatingwebhookconfiguration_metadata_resource_version` | gauge | 12 | mutatingwebhookconfiguration, namespace | Resource version representing a specific version of the MutatingWebhookConfiguration. |
| `kube_mutatingwebhookconfiguration_webhook_clientconfig_service` | gauge | 12 | mutatingwebhookconfiguration, namespace, service_name, service_namespace, webhook_name | Service used by the apiserver to connect to a mutating webhook. |
| `kube_namespace_created` | gauge | 15 | namespace | [STABLE] Unix creation timestamp |
| `kube_namespace_status_phase` | gauge | 30 | namespace, phase | [STABLE] kubernetes namespace status phase. |
| `kube_node_created` | gauge | 12 | node | [STABLE] Unix creation timestamp |
| `kube_node_info` | gauge | 12 | container_runtime_version, internal_ip, kernel_version, kubelet_version, kubeproxy_version, node, os_image, pod_cidr, provider_id, system_uuid | [STABLE] Information about a cluster node. |
| `kube_node_labels` | gauge | 12 | label_beta_kubernetes_io_arch, label_beta_kubernetes_io_os, label_kubernetes_io_arch, label_kubernetes_io_hostname, label_kubernetes_io_os, label_kubernetes_io_role, label_kubernetes_macstadium_com_hosts_type, label_kubernetes_macstadium_com_managed, label_node_kubernetes_io_exclude_from_external_load_balancers, label_node_role_kubernetes_io_control_plane, label_node_role_orka_worker_node, label_orka_macstadium_com_namespace, label_orka_node_tag_cache, label_orka_node_tag_satatest, label_orka_node_tag_virtiotest, label_type, node | [STABLE] Kubernetes labels converted to Prometheus labels. |
| `kube_node_role` | gauge | 3 | node, role | The role of a cluster node. |
| `kube_node_spec_taint` | gauge | 19 | effect, key, node, value | [STABLE] The taint of a cluster node. |
| `kube_node_spec_unschedulable` | gauge | 12 | node | [STABLE] Whether a node can schedule new pods. |
| `kube_node_status_allocatable` | gauge | 66 | node, resource, unit | [STABLE] The allocatable for different resources of a node that are available for scheduling. |
| `kube_node_status_capacity` | gauge | 66 | node, resource, unit | [STABLE] The capacity for different resources of a node. |
| `kube_node_status_condition` | gauge | 195 | condition, node, status | [STABLE] The condition of a cluster node. |
| `kube_pod_completion_time` | gauge | 3 | namespace, pod, uid | [STABLE] Completion time in unix timestamp for a pod. |
| `kube_pod_container_info` | gauge | 74 | container, container_id, image, image_id, image_spec, namespace, pod, uid | [STABLE] Information about a container in a pod. |
| `kube_pod_container_resource_limits` | gauge | 45 | container, namespace, node, pod, resource, uid, unit | The number of requested limit resource by a container. It is recommended to use the kube_pod_resource_limits metric exposed by kube-schedule |
| `kube_pod_container_resource_requests` | gauge | 87 | container, namespace, node, pod, resource, uid, unit | The number of requested request resource by a container. It is recommended to use the kube_pod_resource_requests metric exposed by kube-sche |
| `kube_pod_container_state_started` | gauge | 74 | container, namespace, pod, uid | [STABLE] Start time in unix timestamp for a pod container. |
| `kube_pod_container_status_last_terminated_exitcode` | gauge | 22 | container, namespace, pod, uid | Describes the exit code for the last container in terminated state. |
| `kube_pod_container_status_last_terminated_reason` | gauge | 22 | container, namespace, pod, reason, uid | Describes the last reason the container was in terminated state. |
| `kube_pod_container_status_ready` | gauge | 74 | container, namespace, pod, uid | [STABLE] Describes whether the containers readiness check succeeded. |
| `kube_pod_container_status_restarts_total` | counter | 74 | container, namespace, pod, uid | [STABLE] The number of container restarts per container. |
| `kube_pod_container_status_running` | gauge | 74 | container, namespace, pod, uid | [STABLE] Describes whether the container is currently in running state. |
| `kube_pod_container_status_terminated` | gauge | 74 | container, namespace, pod, uid | [STABLE] Describes whether the container is currently in terminated state. |
| `kube_pod_container_status_terminated_reason` | gauge | 3 | container, namespace, pod, reason, uid | Describes the reason the container is currently in terminated state. |
| `kube_pod_container_status_waiting` | gauge | 74 | container, namespace, pod, uid | [STABLE] Describes whether the container is currently in waiting state. |
| `kube_pod_created` | gauge | 73 | namespace, pod, uid | [STABLE] Unix creation timestamp |
| `kube_pod_info` | gauge | 73 | created_by_kind, created_by_name, host_ip, host_network, namespace, node, pod, pod_ip, priority_class, uid | [STABLE] Information about pod. |
| `kube_pod_init_container_info` | gauge | 22 | container, container_id, image, image_id, image_spec, namespace, pod, uid | [STABLE] Information about an init container in a pod. |
| `kube_pod_init_container_resource_limits` | gauge | 2 | container, namespace, node, pod, resource, uid, unit | The number of requested limit resource by an init container. |
| `kube_pod_init_container_resource_requests` | gauge | 2 | container, namespace, node, pod, resource, uid, unit | The number of requested request resource by an init container. |
| `kube_pod_init_container_status_ready` | gauge | 22 | container, namespace, pod, uid | [STABLE] Describes whether the init containers readiness check succeeded. |
| `kube_pod_init_container_status_restarts_total` | counter | 22 | container, namespace, pod, uid | [STABLE] The number of restarts for the init container. |
| `kube_pod_init_container_status_running` | gauge | 22 | container, namespace, pod, uid | [STABLE] Describes whether the init container is currently in running state. |
| `kube_pod_init_container_status_terminated` | gauge | 22 | container, namespace, pod, uid | [STABLE] Describes whether the init container is currently in terminated state. |
| `kube_pod_init_container_status_terminated_reason` | gauge | 22 | container, namespace, pod, reason, uid | Describes the reason the init container is currently in terminated state. |
| `kube_pod_init_container_status_waiting` | gauge | 22 | container, namespace, pod, uid | [STABLE] Describes whether the init container is currently in waiting state. |
| `kube_pod_ips` | gauge | 71 | ip, ip_family, namespace, pod, uid | Pod IP addresses |
| `kube_pod_owner` | gauge | 73 | namespace, owner_is_controller, owner_kind, owner_name, pod, uid | [STABLE] Information about the Pod's owner. |
| `kube_pod_restart_policy` | gauge | 73 | namespace, pod, type, uid | [STABLE] Describes the restart policy in use by this pod. |
| `kube_pod_service_account` | gauge | 73 | namespace, pod, service_account, uid | The service account for a pod. |
| `kube_pod_start_time` | gauge | 71 | namespace, pod, uid | [STABLE] Start time in unix timestamp for a pod. |
| `kube_pod_status_container_ready_time` | gauge | 68 | namespace, pod, uid | Readiness achieved time in unix timestamp for a pod containers. |
| `kube_pod_status_initialized_time` | gauge | 71 | namespace, pod, uid | Initialized time in unix timestamp for a pod. |
| `kube_pod_status_phase` | gauge | 365 | namespace, phase, pod, uid | [STABLE] The pods current phase. |
| `kube_pod_status_qos_class` | gauge | 219 | namespace, pod, qos_class, uid | The pods current qosClass. |
| `kube_pod_status_ready` | gauge | 213 | condition, namespace, pod, uid | [STABLE] Describes whether the pod is ready to serve requests. |
| `kube_pod_status_ready_time` | gauge | 64 | namespace, pod, uid | Readiness achieved time in unix timestamp for a pod. |
| `kube_pod_status_reason` | gauge | 365 | namespace, pod, reason, uid | The pod status reasons |
| `kube_pod_status_scheduled` | gauge | 219 | condition, namespace, pod, uid | [STABLE] Describes the status of the scheduling process for the pod. |
| `kube_pod_status_scheduled_time` | gauge | 71 | namespace, pod, uid | [STABLE] Unix timestamp when pod moved into scheduled status |
| `kube_pod_status_unschedulable` | gauge | 2 | namespace, pod, uid | [STABLE] Describes the unschedulable status for the pod. |
| `kube_pod_tolerations` | gauge | 381 | effect, key, namespace, operator, pod, toleration_seconds, uid, value | Information about the pod tolerations |
| `kube_poddisruptionbudget_created` | gauge | 1 | namespace, poddisruptionbudget | [STABLE] Unix creation timestamp |
| `kube_poddisruptionbudget_status_current_healthy` | gauge | 1 | namespace, poddisruptionbudget | [STABLE] Current number of healthy pods |
| `kube_poddisruptionbudget_status_desired_healthy` | gauge | 1 | namespace, poddisruptionbudget | [STABLE] Minimum desired number of healthy pods |
| `kube_poddisruptionbudget_status_expected_pods` | gauge | 1 | namespace, poddisruptionbudget | [STABLE] Total number of pods counted by this disruption budget |
| `kube_poddisruptionbudget_status_observed_generation` | gauge | 1 | namespace, poddisruptionbudget | [STABLE] Most recent generation observed when updating this PDB status |
| `kube_poddisruptionbudget_status_pod_disruptions_allowed` | gauge | 1 | namespace, poddisruptionbudget | [STABLE] Number of pod disruptions that are currently allowed |
| `kube_replicaset_created` | gauge | 50 | namespace, replicaset | [STABLE] Unix creation timestamp |
| `kube_replicaset_metadata_generation` | gauge | 50 | namespace, replicaset | [STABLE] Sequence number representing a specific generation of the desired state. |
| `kube_replicaset_owner` | gauge | 50 | namespace, owner_is_controller, owner_kind, owner_name, replicaset | [STABLE] Information about the ReplicaSet's owner. |
| `kube_replicaset_spec_replicas` | gauge | 50 | namespace, replicaset | [STABLE] Number of desired pods for a ReplicaSet. |
| `kube_replicaset_status_fully_labeled_replicas` | gauge | 50 | namespace, replicaset | [STABLE] The number of fully labeled replicas per ReplicaSet. |
| `kube_replicaset_status_observed_generation` | gauge | 50 | namespace, replicaset | [STABLE] The generation observed by the ReplicaSet controller. |
| `kube_replicaset_status_ready_replicas` | gauge | 50 | namespace, replicaset | [STABLE] The number of ready replicas per ReplicaSet. |
| `kube_replicaset_status_replicas` | gauge | 50 | namespace, replicaset | [STABLE] The number of replicas per ReplicaSet. |
| `kube_secret_created` | gauge | 48 | namespace, secret | [STABLE] Unix creation timestamp |
| `kube_secret_info` | gauge | 48 | namespace, secret | [STABLE] Information about secret. |
| `kube_secret_metadata_resource_version` | gauge | 48 | namespace, secret | Resource version representing a specific version of secret. |
| `kube_secret_type` | gauge | 48 | namespace, secret, type | [STABLE] Type about secret. |
| `kube_service_created` | gauge | 30 | namespace, service, uid | [STABLE] Unix creation timestamp |
| `kube_service_info` | gauge | 30 | cluster_ip, external_name, load_balancer_ip, namespace, service, uid | [STABLE] Information about service. |
| `kube_service_spec_external_ip` | gauge | 1 | external_ip, namespace, service, uid | [STABLE] Service external ips. One series for each ip |
| `kube_service_spec_type` | gauge | 30 | namespace, service, type, uid | [STABLE] Type about service. |
| `kube_service_status_load_balancer_ingress` | gauge | 7 | hostname, ip, namespace, service, uid | [STABLE] Service load balancer ingress status |
| `kube_statefulset_created` | gauge | 1 | namespace, statefulset | [STABLE] Unix creation timestamp |
| `kube_statefulset_metadata_generation` | gauge | 1 | namespace, statefulset | [STABLE] Sequence number representing a specific generation of the desired state for the StatefulSet. |
| `kube_statefulset_persistentvolumeclaim_retention_policy` | gauge | 1 | namespace, statefulset, when_deleted, when_scaled | Count of retention policy for StatefulSet template PVCs |
| `kube_statefulset_replicas` | gauge | 1 | namespace, statefulset | [STABLE] Number of desired pods for a StatefulSet. |
| `kube_statefulset_status_current_revision` | gauge | 1 | namespace, revision, statefulset | [STABLE] Indicates the version of the StatefulSet used to generate Pods in the sequence [0,currentReplicas). |
| `kube_statefulset_status_observed_generation` | gauge | 1 | namespace, statefulset | [STABLE] The generation observed by the StatefulSet controller. |
| `kube_statefulset_status_replicas` | gauge | 1 | namespace, statefulset | [STABLE] The number of replicas per StatefulSet. |
| `kube_statefulset_status_replicas_available` | gauge | 1 | namespace, statefulset | The number of available replicas per StatefulSet. |
| `kube_statefulset_status_replicas_current` | gauge | 1 | namespace, statefulset | [STABLE] The number of current replicas per StatefulSet. |
| `kube_statefulset_status_replicas_ready` | gauge | 1 | namespace, statefulset | [STABLE] The number of ready replicas per StatefulSet. |
| `kube_statefulset_status_replicas_updated` | gauge | 1 | namespace, statefulset | [STABLE] The number of updated replicas per StatefulSet. |
| `kube_statefulset_status_update_revision` | gauge | 1 | namespace, revision, statefulset | [STABLE] Indicates the version of the StatefulSet used to generate Pods in the sequence [replicas-updatedReplicas,replicas) |
| `kube_validatingwebhookconfiguration_created` | gauge | 13 | namespace, validatingwebhookconfiguration | Unix creation timestamp. |
| `kube_validatingwebhookconfiguration_info` | gauge | 13 | namespace, validatingwebhookconfiguration | Information about the ValidatingWebhookConfiguration. |
| `kube_validatingwebhookconfiguration_metadata_resource_version` | gauge | 13 | namespace, validatingwebhookconfiguration | Resource version representing a specific version of the ValidatingWebhookConfiguration. |
| `kube_validatingwebhookconfiguration_webhook_clientconfig_service` | gauge | 18 | namespace, service_name, service_namespace, validatingwebhookconfiguration, webhook_name | Service used by the apiserver to connect to a validating webhook. |

Example raw lines:

```
# TYPE kube_node_status_condition gauge
kube_node_status_condition{node="x86-mini-4",condition="NetworkUnavailable",status="true"} 0
# TYPE kube_pod_container_resource_requests gauge
kube_pod_container_resource_requests{namespace="kube-system",pod="calico-node-6p56c",uid="7a0572be-3aed-4f6f-a992-83f28725e0b8",container="calico-node",node="x86-mini-1",
# TYPE kube_pod_info gauge
kube_pod_info{namespace="monitoring",pod="kps-prometheus-node-exporter-q7j6r",uid="3a4b3ba4-4eb1-4966-963f-9b402c3ab0b4",host_ip="10.221.192.31",pod_ip="10.221.192.31",no
# TYPE kube_pod_status_phase gauge
kube_pod_status_phase{namespace="default",pod="orka-webhooks-6665fd8c6f-q4888",uid="7d3f47af-844b-4bc9-b578-c0b4a7d39719",phase="Pending"} 0
```

## blackbox-exporter

Endpoint: `http://<orka LB IP>:9115/metrics`

Documented customer endpoint. The exporter's own metrics; probe results exist only when a Probe/target is queried.

**40 metric families, 48 series** in this capture.

| Family | Type | Series | Label keys | Help |
|---|---|---|---|---|
| `blackbox_exporter_build_info` | gauge | 1 | branch, goversion, revision, version | A metric with a constant '1' value labeled by version, revision, branch, and goversion from which blackbox_exporter was built. |
| `blackbox_exporter_config_last_reload_success_timestamp_seconds` | gauge | 1 | — | Timestamp of the last successful configuration reload. |
| `blackbox_exporter_config_last_reload_successful` | gauge | 1 | — | Blackbox exporter config loaded successfully. |
| `blackbox_module_unknown_total` | counter | 1 | — | Count of unknown modules requested by probes |
| `go_gc_duration_seconds` | summary | 7 | quantile | A summary of the pause duration of garbage collection cycles. |
| `go_goroutines` | gauge | 1 | — | Number of goroutines that currently exist. |
| `go_info` | gauge | 1 | version | Information about the Go environment. |
| `go_memstats_alloc_bytes` | gauge | 1 | — | Number of bytes allocated and still in use. |
| `go_memstats_alloc_bytes_total` | counter | 1 | — | Total number of bytes allocated, even if freed. |
| `go_memstats_buck_hash_sys_bytes` | gauge | 1 | — | Number of bytes used by the profiling bucket hash table. |
| `go_memstats_frees_total` | counter | 1 | — | Total number of frees. |
| `go_memstats_gc_sys_bytes` | gauge | 1 | — | Number of bytes used for garbage collection system metadata. |
| `go_memstats_heap_alloc_bytes` | gauge | 1 | — | Number of heap bytes allocated and still in use. |
| `go_memstats_heap_idle_bytes` | gauge | 1 | — | Number of heap bytes waiting to be used. |
| `go_memstats_heap_inuse_bytes` | gauge | 1 | — | Number of heap bytes that are in use. |
| `go_memstats_heap_objects` | gauge | 1 | — | Number of allocated objects. |
| `go_memstats_heap_released_bytes` | gauge | 1 | — | Number of heap bytes released to OS. |
| `go_memstats_heap_sys_bytes` | gauge | 1 | — | Number of heap bytes obtained from system. |
| `go_memstats_last_gc_time_seconds` | gauge | 1 | — | Number of seconds since 1970 of last garbage collection. |
| `go_memstats_lookups_total` | counter | 1 | — | Total number of pointer lookups. |
| `go_memstats_mallocs_total` | counter | 1 | — | Total number of mallocs. |
| `go_memstats_mcache_inuse_bytes` | gauge | 1 | — | Number of bytes in use by mcache structures. |
| `go_memstats_mcache_sys_bytes` | gauge | 1 | — | Number of bytes used for mcache structures obtained from system. |
| `go_memstats_mspan_inuse_bytes` | gauge | 1 | — | Number of bytes in use by mspan structures. |
| `go_memstats_mspan_sys_bytes` | gauge | 1 | — | Number of bytes used for mspan structures obtained from system. |
| `go_memstats_next_gc_bytes` | gauge | 1 | — | Number of heap bytes when next garbage collection will take place. |
| `go_memstats_other_sys_bytes` | gauge | 1 | — | Number of bytes used for other system allocations. |
| `go_memstats_stack_inuse_bytes` | gauge | 1 | — | Number of bytes in use by the stack allocator. |
| `go_memstats_stack_sys_bytes` | gauge | 1 | — | Number of bytes obtained from system for stack allocator. |
| `go_memstats_sys_bytes` | gauge | 1 | — | Number of bytes obtained from system. |
| `go_threads` | gauge | 1 | — | Number of OS threads created. |
| `process_cpu_seconds_total` | counter | 1 | — | Total user and system CPU time spent in seconds. |
| `process_max_fds` | gauge | 1 | — | Maximum number of open file descriptors. |
| `process_open_fds` | gauge | 1 | — | Number of open file descriptors. |
| `process_resident_memory_bytes` | gauge | 1 | — | Resident memory size in bytes. |
| `process_start_time_seconds` | gauge | 1 | — | Start time of the process since unix epoch in seconds. |
| `process_virtual_memory_bytes` | gauge | 1 | — | Virtual memory size in bytes. |
| `process_virtual_memory_max_bytes` | gauge | 1 | — | Maximum amount of virtual memory available in bytes. |
| `promhttp_metric_handler_requests_in_flight` | gauge | 1 | — | Current number of scrapes being served. |
| `promhttp_metric_handler_requests_total` | counter | 3 | code | Total number of scrapes by HTTP status code. |

Example raw lines:

```
# TYPE blackbox_exporter_build_info gauge
blackbox_exporter_build_info{branch="HEAD",goversion="go1.19.3",revision="26fc98b9c6db21457653ed752f34d1b7fb5bba43",version="0.23.0"} 1
# TYPE go_goroutines gauge
go_goroutines 11
```

## Orka API server (via ingress)

Endpoint: `https://<orka ingress IP>/api/v1/metrics`

Go runtime/process metrics only. Sources describe the route as auth-gated; on L20 it answered 200 without a token.

**38 metric families, 44 series** in this capture.

| Family | Type | Series | Label keys | Help |
|---|---|---|---|---|
| `go_gc_duration_seconds` | summary | 7 | quantile | A summary of the wall-time pause (stop-the-world) duration in garbage collection cycles. |
| `go_gc_gogc_percent` | gauge | 1 | — | Heap size target percentage configured by the user, otherwise 100. This value is set by the GOGC environment variable, and the runtime/debug |
| `go_gc_gomemlimit_bytes` | gauge | 1 | — | Go runtime memory limit configured by the user, otherwise math.MaxInt64. This value is set by the GOMEMLIMIT environment variable, and the r |
| `go_goroutines` | gauge | 1 | — | Number of goroutines that currently exist. |
| `go_info` | gauge | 1 | version | Information about the Go environment. |
| `go_memstats_alloc_bytes` | gauge | 1 | — | Number of bytes allocated in heap and currently in use. Equals to /memory/classes/heap/objects:bytes. |
| `go_memstats_alloc_bytes_total` | counter | 1 | — | Total number of bytes allocated in heap until now, even if released already. Equals to /gc/heap/allocs:bytes. |
| `go_memstats_buck_hash_sys_bytes` | gauge | 1 | — | Number of bytes used by the profiling bucket hash table. Equals to /memory/classes/profiling/buckets:bytes. |
| `go_memstats_frees_total` | counter | 1 | — | Total number of heap objects frees. Equals to /gc/heap/frees:objects + /gc/heap/tiny/allocs:objects. |
| `go_memstats_gc_sys_bytes` | gauge | 1 | — | Number of bytes used for garbage collection system metadata. Equals to /memory/classes/metadata/other:bytes. |
| `go_memstats_heap_alloc_bytes` | gauge | 1 | — | Number of heap bytes allocated and currently in use, same as go_memstats_alloc_bytes. Equals to /memory/classes/heap/objects:bytes. |
| `go_memstats_heap_idle_bytes` | gauge | 1 | — | Number of heap bytes waiting to be used. Equals to /memory/classes/heap/released:bytes + /memory/classes/heap/free:bytes. |
| `go_memstats_heap_inuse_bytes` | gauge | 1 | — | Number of heap bytes that are in use. Equals to /memory/classes/heap/objects:bytes + /memory/classes/heap/unused:bytes |
| `go_memstats_heap_objects` | gauge | 1 | — | Number of currently allocated objects. Equals to /gc/heap/objects:objects. |
| `go_memstats_heap_released_bytes` | gauge | 1 | — | Number of heap bytes released to OS. Equals to /memory/classes/heap/released:bytes. |
| `go_memstats_heap_sys_bytes` | gauge | 1 | — | Number of heap bytes obtained from system. Equals to /memory/classes/heap/objects:bytes + /memory/classes/heap/unused:bytes + /memory/classe |
| `go_memstats_last_gc_time_seconds` | gauge | 1 | — | Number of seconds since 1970 of last garbage collection. |
| `go_memstats_mallocs_total` | counter | 1 | — | Total number of heap objects allocated, both live and gc-ed. Semantically a counter version for go_memstats_heap_objects gauge. Equals to /g |
| `go_memstats_mcache_inuse_bytes` | gauge | 1 | — | Number of bytes in use by mcache structures. Equals to /memory/classes/metadata/mcache/inuse:bytes. |
| `go_memstats_mcache_sys_bytes` | gauge | 1 | — | Number of bytes used for mcache structures obtained from system. Equals to /memory/classes/metadata/mcache/inuse:bytes + /memory/classes/met |
| `go_memstats_mspan_inuse_bytes` | gauge | 1 | — | Number of bytes in use by mspan structures. Equals to /memory/classes/metadata/mspan/inuse:bytes. |
| `go_memstats_mspan_sys_bytes` | gauge | 1 | — | Number of bytes used for mspan structures obtained from system. Equals to /memory/classes/metadata/mspan/inuse:bytes + /memory/classes/metad |
| `go_memstats_next_gc_bytes` | gauge | 1 | — | Number of heap bytes when next garbage collection will take place. Equals to /gc/heap/goal:bytes. |
| `go_memstats_other_sys_bytes` | gauge | 1 | — | Number of bytes used for other system allocations. Equals to /memory/classes/other:bytes. |
| `go_memstats_stack_inuse_bytes` | gauge | 1 | — | Number of bytes obtained from system for stack allocator in non-CGO environments. Equals to /memory/classes/heap/stacks:bytes. |
| `go_memstats_stack_sys_bytes` | gauge | 1 | — | Number of bytes obtained from system for stack allocator. Equals to /memory/classes/heap/stacks:bytes + /memory/classes/os-stacks:bytes. |
| `go_memstats_sys_bytes` | gauge | 1 | — | Number of bytes obtained from system. Equals to /memory/classes/total:byte. |
| `go_sched_gomaxprocs_threads` | gauge | 1 | — | The current runtime.GOMAXPROCS setting, or the number of operating system threads that can execute user-level Go code simultaneously. Source |
| `go_threads` | gauge | 1 | — | Number of OS threads created. |
| `process_cpu_seconds_total` | counter | 1 | — | Total user and system CPU time spent in seconds. |
| `process_max_fds` | gauge | 1 | — | Maximum number of open file descriptors. |
| `process_network_receive_bytes_total` | counter | 1 | — | Number of bytes received by the process over the network. |
| `process_network_transmit_bytes_total` | counter | 1 | — | Number of bytes sent by the process over the network. |
| `process_open_fds` | gauge | 1 | — | Number of open file descriptors. |
| `process_resident_memory_bytes` | gauge | 1 | — | Resident memory size in bytes. |
| `process_start_time_seconds` | gauge | 1 | — | Start time of the process since unix epoch in seconds. |
| `process_virtual_memory_bytes` | gauge | 1 | — | Virtual memory size in bytes. |
| `process_virtual_memory_max_bytes` | gauge | 1 | — | Maximum amount of virtual memory available in bytes. |

Example raw lines:

```
# TYPE go_goroutines gauge
go_goroutines 9
```

## node_exporter — macOS (Apple silicon host)

Endpoint: `http://<node IP>:9100/metrics`

Host metrics from a macOS node (L20 arm-mini-005).

**90 metric families, 486 series** in this capture.

| Family | Type | Series | Label keys | Help |
|---|---|---|---|---|
| `go_gc_duration_seconds` | summary | 7 | quantile | A summary of the wall-time pause (stop-the-world) duration in garbage collection cycles. |
| `go_gc_gogc_percent` | gauge | 1 | — | Heap size target percentage configured by the user, otherwise 100. This value is set by the GOGC environment variable, and the runtime/debug |
| `go_gc_gomemlimit_bytes` | gauge | 1 | — | Go runtime memory limit configured by the user, otherwise math.MaxInt64. This value is set by the GOMEMLIMIT environment variable, and the r |
| `go_goroutines` | gauge | 1 | — | Number of goroutines that currently exist. |
| `go_info` | gauge | 1 | version | Information about the Go environment. |
| `go_memstats_alloc_bytes` | gauge | 1 | — | Number of bytes allocated in heap and currently in use. Equals to /memory/classes/heap/objects:bytes. |
| `go_memstats_alloc_bytes_total` | counter | 1 | — | Total number of bytes allocated in heap until now, even if released already. Equals to /gc/heap/allocs:bytes. |
| `go_memstats_buck_hash_sys_bytes` | gauge | 1 | — | Number of bytes used by the profiling bucket hash table. Equals to /memory/classes/profiling/buckets:bytes. |
| `go_memstats_frees_total` | counter | 1 | — | Total number of heap objects frees. Equals to /gc/heap/frees:objects + /gc/heap/tiny/allocs:objects. |
| `go_memstats_gc_sys_bytes` | gauge | 1 | — | Number of bytes used for garbage collection system metadata. Equals to /memory/classes/metadata/other:bytes. |
| `go_memstats_heap_alloc_bytes` | gauge | 1 | — | Number of heap bytes allocated and currently in use, same as go_memstats_alloc_bytes. Equals to /memory/classes/heap/objects:bytes. |
| `go_memstats_heap_idle_bytes` | gauge | 1 | — | Number of heap bytes waiting to be used. Equals to /memory/classes/heap/released:bytes + /memory/classes/heap/free:bytes. |
| `go_memstats_heap_inuse_bytes` | gauge | 1 | — | Number of heap bytes that are in use. Equals to /memory/classes/heap/objects:bytes + /memory/classes/heap/unused:bytes |
| `go_memstats_heap_objects` | gauge | 1 | — | Number of currently allocated objects. Equals to /gc/heap/objects:objects. |
| `go_memstats_heap_released_bytes` | gauge | 1 | — | Number of heap bytes released to OS. Equals to /memory/classes/heap/released:bytes. |
| `go_memstats_heap_sys_bytes` | gauge | 1 | — | Number of heap bytes obtained from system. Equals to /memory/classes/heap/objects:bytes + /memory/classes/heap/unused:bytes + /memory/classe |
| `go_memstats_last_gc_time_seconds` | gauge | 1 | — | Number of seconds since 1970 of last garbage collection. |
| `go_memstats_mallocs_total` | counter | 1 | — | Total number of heap objects allocated, both live and gc-ed. Semantically a counter version for go_memstats_heap_objects gauge. Equals to /g |
| `go_memstats_mcache_inuse_bytes` | gauge | 1 | — | Number of bytes in use by mcache structures. Equals to /memory/classes/metadata/mcache/inuse:bytes. |
| `go_memstats_mcache_sys_bytes` | gauge | 1 | — | Number of bytes used for mcache structures obtained from system. Equals to /memory/classes/metadata/mcache/inuse:bytes + /memory/classes/met |
| `go_memstats_mspan_inuse_bytes` | gauge | 1 | — | Number of bytes in use by mspan structures. Equals to /memory/classes/metadata/mspan/inuse:bytes. |
| `go_memstats_mspan_sys_bytes` | gauge | 1 | — | Number of bytes used for mspan structures obtained from system. Equals to /memory/classes/metadata/mspan/inuse:bytes + /memory/classes/metad |
| `go_memstats_next_gc_bytes` | gauge | 1 | — | Number of heap bytes when next garbage collection will take place. Equals to /gc/heap/goal:bytes. |
| `go_memstats_other_sys_bytes` | gauge | 1 | — | Number of bytes used for other system allocations. Equals to /memory/classes/other:bytes. |
| `go_memstats_stack_inuse_bytes` | gauge | 1 | — | Number of bytes obtained from system for stack allocator in non-CGO environments. Equals to /memory/classes/heap/stacks:bytes. |
| `go_memstats_stack_sys_bytes` | gauge | 1 | — | Number of bytes obtained from system for stack allocator. Equals to /memory/classes/heap/stacks:bytes + /memory/classes/os-stacks:bytes. |
| `go_memstats_sys_bytes` | gauge | 1 | — | Number of bytes obtained from system. Equals to /memory/classes/total:byte. |
| `go_sched_gomaxprocs_threads` | gauge | 1 | — | The current runtime.GOMAXPROCS setting, or the number of operating system threads that can execute user-level Go code simultaneously. Source |
| `go_threads` | gauge | 1 | — | Number of OS threads created. |
| `node_boot_time_seconds` | gauge | 1 | — | Unix time of last boot, including microseconds. |
| `node_cpu_seconds_total` | counter | 32 | cpu, mode | Seconds the CPUs spent in each mode. |
| `node_disk_read_bytes_total` | counter | 1 | device | The total number of bytes read successfully. |
| `node_disk_read_errors_total` | counter | 1 | device | The total number of read errors. |
| `node_disk_read_retries_total` | counter | 1 | device | The total number of read retries. |
| `node_disk_read_sectors_total` | counter | 1 | device | The total number of sectors read successfully. |
| `node_disk_read_time_seconds_total` | counter | 1 | device | The total number of seconds spent by all reads. |
| `node_disk_reads_completed_total` | counter | 1 | device | The total number of reads completed successfully. |
| `node_disk_write_errors_total` | counter | 1 | device | The total number of write errors. |
| `node_disk_write_retries_total` | counter | 1 | device | The total number of write retries. |
| `node_disk_write_time_seconds_total` | counter | 1 | device | This is the total number of seconds spent by all writes. |
| `node_disk_writes_completed_total` | counter | 1 | device | The total number of writes completed successfully. |
| `node_disk_written_bytes_total` | counter | 1 | device | The total number of bytes written successfully. |
| `node_disk_written_sectors_total` | counter | 1 | device | The total number of sectors written successfully. |
| `node_exporter_build_info` | gauge | 1 | branch, goarch, goos, goversion, revision, tags, version | A metric with a constant '1' value labeled by version, revision, branch, goversion from which node_exporter was built, and the goos and goar |
| `node_filesystem_avail_bytes` | gauge | 11 | device, device_error, fstype, mountpoint | Filesystem space available to non-root users in bytes. |
| `node_filesystem_device_error` | gauge | 11 | device, device_error, fstype, mountpoint | Whether an error occurred while getting statistics for the given device. |
| `node_filesystem_files` | gauge | 11 | device, device_error, fstype, mountpoint | Filesystem total file nodes. |
| `node_filesystem_files_free` | gauge | 11 | device, device_error, fstype, mountpoint | Filesystem total free file nodes. |
| `node_filesystem_free_bytes` | gauge | 11 | device, device_error, fstype, mountpoint | Filesystem free space in bytes. |
| `node_filesystem_mount_info` | gauge | 11 | device, major, minor, mountpoint | Filesystem mount information. |
| `node_filesystem_purgeable_bytes` | gauge | 11 | device, device_error, fstype, mountpoint | Filesystem space available including purgeable space (MacOS specific). |
| `node_filesystem_readonly` | gauge | 11 | device, device_error, fstype, mountpoint | Filesystem read-only status. |
| `node_filesystem_size_bytes` | gauge | 11 | device, device_error, fstype, mountpoint | Filesystem size in bytes. |
| `node_load1` | gauge | 1 | — | 1m load average. |
| `node_load15` | gauge | 1 | — | 15m load average. |
| `node_load5` | gauge | 1 | — | 5m load average. |
| `node_memory_active_bytes` | gauge | 1 | — | Memory information field active_bytes. |
| `node_memory_compressed_bytes` | gauge | 1 | — | Memory information field compressed_bytes. |
| `node_memory_free_bytes` | gauge | 1 | — | Memory information field free_bytes. |
| `node_memory_inactive_bytes` | gauge | 1 | — | Memory information field inactive_bytes. |
| `node_memory_internal_bytes` | gauge | 1 | — | Memory information field internal_bytes. |
| `node_memory_purgeable_bytes` | gauge | 1 | — | Memory information field purgeable_bytes. |
| `node_memory_swap_total_bytes` | gauge | 1 | — | Memory information field swap_total_bytes. |
| `node_memory_swap_used_bytes` | gauge | 1 | — | Memory information field swap_used_bytes. |
| `node_memory_swapped_in_bytes_total` | counter | 1 | — | Memory information field swapped_in_bytes_total. |
| `node_memory_swapped_out_bytes_total` | counter | 1 | — | Memory information field swapped_out_bytes_total. |
| `node_memory_total_bytes` | gauge | 1 | — | Memory information field total_bytes. |
| `node_memory_wired_bytes` | gauge | 1 | — | Memory information field wired_bytes. |
| `node_network_noproto_total` | counter | 23 | device | Network device statistic noproto. |
| `node_network_receive_bytes_total` | counter | 23 | device | Network device statistic receive_bytes. |
| `node_network_receive_drop_total` | counter | 23 | device | Network device statistic receive_drop. |
| `node_network_receive_errs_total` | counter | 23 | device | Network device statistic receive_errs. |
| `node_network_receive_multicast_total` | counter | 23 | device | Network device statistic receive_multicast. |
| `node_network_receive_packets_total` | counter | 23 | device | Network device statistic receive_packets. |
| `node_network_transmit_bytes_total` | counter | 23 | device | Network device statistic transmit_bytes. |
| `node_network_transmit_colls_total` | counter | 23 | device | Network device statistic transmit_colls. |
| `node_network_transmit_errs_total` | counter | 23 | device | Network device statistic transmit_errs. |
| `node_network_transmit_multicast_total` | counter | 23 | device | Network device statistic transmit_multicast. |
| `node_network_transmit_packets_total` | counter | 23 | device | Network device statistic transmit_packets. |
| `node_os_info` | gauge | 1 | build_id, id, id_like, image_id, image_version, name, pretty_name, variant, variant_id, version, version_codename, version_id | A metric with a constant '1' value labeled by build_id, id, id_like, image_id, image_version, name, pretty_name, variant, variant_id, versio |
| `node_os_version` | gauge | 1 | id, id_like, name | Metric containing the major.minor part of the OS version. |
| `node_scrape_collector_duration_seconds` | gauge | 13 | collector | node_exporter: Duration of a collector scrape. |
| `node_scrape_collector_success` | gauge | 13 | collector | node_exporter: Whether a collector succeeded. |
| `node_textfile_scrape_error` | gauge | 1 | — | 1 if there was an error opening or reading a file, 0 otherwise |
| `node_time_seconds` | gauge | 1 | — | System time in seconds since epoch (1970). |
| `node_time_zone_offset_seconds` | gauge | 1 | time_zone | System time zone offset in seconds. |
| `node_uname_info` | gauge | 1 | domainname, machine, nodename, release, sysname, version | Labeled system information as provided by the uname system call. |
| `promhttp_metric_handler_errors_total` | counter | 2 | cause | Total number of internal errors encountered by the promhttp metric handler. |
| `promhttp_metric_handler_requests_in_flight` | gauge | 1 | — | Current number of scrapes being served. |
| `promhttp_metric_handler_requests_total` | counter | 3 | code | Total number of scrapes by HTTP status code. |

Example raw lines:

```
# TYPE go_goroutines gauge
go_goroutines 9
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="idle"} 2.75000785e+06
# TYPE node_filesystem_avail_bytes gauge
node_filesystem_avail_bytes{device="/dev/disk1s1",device_error="",fstype="apfs",mountpoint="/System/Volumes/iSCPreboot"} 5.05987072e+08
# TYPE node_load1 gauge
node_load1 1.55810546875
# TYPE node_load15 gauge
node_load15 1.58740234375
# TYPE node_memory_total_bytes gauge
node_memory_total_bytes 1.7179869184e+10
```

## node_exporter — Linux (x86 node)

Endpoint: `http://<node IP>:9100/metrics`

Host metrics from a Linux node (L20 x86-mini-1).

**359 metric families, 1194 series** in this capture.

| Family | Type | Series | Label keys | Help |
|---|---|---|---|---|
| `go_gc_duration_seconds` | summary | 7 | quantile | A summary of the pause duration of garbage collection cycles. |
| `go_goroutines` | gauge | 1 | — | Number of goroutines that currently exist. |
| `go_info` | gauge | 1 | version | Information about the Go environment. |
| `go_memstats_alloc_bytes` | gauge | 1 | — | Number of bytes allocated and still in use. |
| `go_memstats_alloc_bytes_total` | counter | 1 | — | Total number of bytes allocated, even if freed. |
| `go_memstats_buck_hash_sys_bytes` | gauge | 1 | — | Number of bytes used by the profiling bucket hash table. |
| `go_memstats_frees_total` | counter | 1 | — | Total number of frees. |
| `go_memstats_gc_sys_bytes` | gauge | 1 | — | Number of bytes used for garbage collection system metadata. |
| `go_memstats_heap_alloc_bytes` | gauge | 1 | — | Number of heap bytes allocated and still in use. |
| `go_memstats_heap_idle_bytes` | gauge | 1 | — | Number of heap bytes waiting to be used. |
| `go_memstats_heap_inuse_bytes` | gauge | 1 | — | Number of heap bytes that are in use. |
| `go_memstats_heap_objects` | gauge | 1 | — | Number of allocated objects. |
| `go_memstats_heap_released_bytes` | gauge | 1 | — | Number of heap bytes released to OS. |
| `go_memstats_heap_sys_bytes` | gauge | 1 | — | Number of heap bytes obtained from system. |
| `go_memstats_last_gc_time_seconds` | gauge | 1 | — | Number of seconds since 1970 of last garbage collection. |
| `go_memstats_lookups_total` | counter | 1 | — | Total number of pointer lookups. |
| `go_memstats_mallocs_total` | counter | 1 | — | Total number of mallocs. |
| `go_memstats_mcache_inuse_bytes` | gauge | 1 | — | Number of bytes in use by mcache structures. |
| `go_memstats_mcache_sys_bytes` | gauge | 1 | — | Number of bytes used for mcache structures obtained from system. |
| `go_memstats_mspan_inuse_bytes` | gauge | 1 | — | Number of bytes in use by mspan structures. |
| `go_memstats_mspan_sys_bytes` | gauge | 1 | — | Number of bytes used for mspan structures obtained from system. |
| `go_memstats_next_gc_bytes` | gauge | 1 | — | Number of heap bytes when next garbage collection will take place. |
| `go_memstats_other_sys_bytes` | gauge | 1 | — | Number of bytes used for other system allocations. |
| `go_memstats_stack_inuse_bytes` | gauge | 1 | — | Number of bytes in use by the stack allocator. |
| `go_memstats_stack_sys_bytes` | gauge | 1 | — | Number of bytes obtained from system for stack allocator. |
| `go_memstats_sys_bytes` | gauge | 1 | — | Number of bytes obtained from system. |
| `go_threads` | gauge | 1 | — | Number of OS threads created. |
| `node_boot_time_seconds` | gauge | 1 | — | Node boot time, in unixtime. |
| `node_context_switches_total` | counter | 1 | — | Total number of context switches. |
| `node_cooling_device_cur_state` | gauge | 13 | name, type | Current throttle state of the cooling device |
| `node_cooling_device_max_state` | gauge | 13 | name, type | Maximum throttle state of the cooling device |
| `node_cpu_core_throttles_total` | counter | 6 | core, package | Number of times this CPU core has been throttled. |
| `node_cpu_frequency_max_hertz` | gauge | 12 | cpu | Maximum CPU thread frequency in hertz. |
| `node_cpu_frequency_min_hertz` | gauge | 12 | cpu | Minimum CPU thread frequency in hertz. |
| `node_cpu_guest_seconds_total` | counter | 24 | cpu, mode | Seconds the CPUs spent in guests (VMs) for each mode. |
| `node_cpu_package_throttles_total` | counter | 1 | package | Number of times this CPU package has been throttled. |
| `node_cpu_scaling_frequency_hertz` | gauge | 12 | cpu | Current scaled CPU thread frequency in hertz. |
| `node_cpu_scaling_frequency_max_hertz` | gauge | 12 | cpu | Maximum scaled CPU thread frequency in hertz. |
| `node_cpu_scaling_frequency_min_hertz` | gauge | 12 | cpu | Minimum scaled CPU thread frequency in hertz. |
| `node_cpu_scaling_governor` | gauge | 24 | cpu, governor | Current enabled CPU frequency governor. |
| `node_cpu_seconds_total` | counter | 96 | cpu, mode | Seconds the CPUs spent in each mode. |
| `node_disk_discard_time_seconds_total` | counter | 1 | device | This is the total number of seconds spent by all discards. |
| `node_disk_discarded_sectors_total` | counter | 1 | device | The total number of sectors discarded successfully. |
| `node_disk_discards_completed_total` | counter | 1 | device | The total number of discards completed successfully. |
| `node_disk_discards_merged_total` | counter | 1 | device | The total number of discards merged. |
| `node_disk_flush_requests_time_seconds_total` | counter | 1 | device | This is the total number of seconds spent by all flush requests. |
| `node_disk_flush_requests_total` | counter | 1 | device | The total number of flush requests completed successfully |
| `node_disk_info` | gauge | 1 | device, major, minor, model, path, revision, serial, wwn | Info of /sys/block/<block_device>. |
| `node_disk_io_now` | gauge | 1 | device | The number of I/Os currently in progress. |
| `node_disk_io_time_seconds_total` | counter | 1 | device | Total seconds spent doing I/Os. |
| `node_disk_io_time_weighted_seconds_total` | counter | 1 | device | The weighted # of seconds spent doing I/Os. |
| `node_disk_read_bytes_total` | counter | 1 | device | The total number of bytes read successfully. |
| `node_disk_read_time_seconds_total` | counter | 1 | device | The total number of seconds spent by all reads. |
| `node_disk_reads_completed_total` | counter | 1 | device | The total number of reads completed successfully. |
| `node_disk_reads_merged_total` | counter | 1 | device | The total number of reads merged. |
| `node_disk_write_time_seconds_total` | counter | 1 | device | This is the total number of seconds spent by all writes. |
| `node_disk_writes_completed_total` | counter | 1 | device | The total number of writes completed successfully. |
| `node_disk_writes_merged_total` | counter | 1 | device | The number of writes merged. |
| `node_disk_written_bytes_total` | counter | 1 | device | The total number of bytes written successfully. |
| `node_dmi_info` | gauge | 1 | bios_date, bios_vendor, bios_version, board_asset_tag, board_name, board_vendor, board_version, chassis_asset_tag, chassis_vendor, chassis_version, product_family, product_name, product_sku, product_version, system_vendor | A metric with a constant '1' value labeled by bios_date, bios_release, bios_vendor, bios_version, board_asset_tag, board_name, board_serial, |
| `node_entropy_available_bits` | gauge | 1 | — | Bits of available entropy. |
| `node_entropy_pool_size_bits` | gauge | 1 | — | Bits of entropy pool. |
| `node_exporter_build_info` | gauge | 1 | branch, goarch, goos, goversion, revision, tags, version | A metric with a constant '1' value labeled by version, revision, branch, goversion from which node_exporter was built, and the goos and goar |
| `node_filefd_allocated` | gauge | 1 | — | File descriptor statistics: allocated. |
| `node_filefd_maximum` | gauge | 1 | — | File descriptor statistics: maximum. |
| `node_filesystem_avail_bytes` | gauge | 8 | device, fstype, mountpoint | Filesystem space available to non-root users in bytes. |
| `node_filesystem_device_error` | gauge | 8 | device, fstype, mountpoint | Whether an error occurred while getting statistics for the given device. |
| `node_filesystem_files` | gauge | 8 | device, fstype, mountpoint | Filesystem total file nodes. |
| `node_filesystem_files_free` | gauge | 8 | device, fstype, mountpoint | Filesystem total free file nodes. |
| `node_filesystem_free_bytes` | gauge | 8 | device, fstype, mountpoint | Filesystem free space in bytes. |
| `node_filesystem_readonly` | gauge | 8 | device, fstype, mountpoint | Filesystem read-only status. |
| `node_filesystem_size_bytes` | gauge | 8 | device, fstype, mountpoint | Filesystem size in bytes. |
| `node_forks_total` | counter | 1 | — | Total number of forks. |
| `node_hwmon_chip_names` | gauge | 4 | chip, chip_name | Annotation metric for human-readable chip names |
| `node_hwmon_sensor_label` | gauge | 9 | chip, label, sensor | Label for given chip and sensor |
| `node_hwmon_temp_alarm` | gauge | 1 | chip, sensor | Hardware sensor alarm status (temp) |
| `node_hwmon_temp_celsius` | gauge | 11 | chip, sensor | Hardware monitor for temperature (input) |
| `node_hwmon_temp_crit_alarm_celsius` | gauge | 7 | chip, sensor | Hardware monitor for temperature (crit_alarm) |
| `node_hwmon_temp_crit_celsius` | gauge | 7 | chip, sensor | Hardware monitor for temperature (crit) |
| `node_hwmon_temp_max_celsius` | gauge | 7 | chip, sensor | Hardware monitor for temperature (max) |
| `node_intr_total` | counter | 1 | — | Total number of interrupts serviced. |
| `node_load1` | gauge | 1 | — | 1m load average. |
| `node_load15` | gauge | 1 | — | 15m load average. |
| `node_load5` | gauge | 1 | — | 5m load average. |
| `node_memory_Active_anon_bytes` | gauge | 1 | — | Memory information field Active_anon_bytes. |
| `node_memory_Active_bytes` | gauge | 1 | — | Memory information field Active_bytes. |
| `node_memory_Active_file_bytes` | gauge | 1 | — | Memory information field Active_file_bytes. |
| `node_memory_AnonHugePages_bytes` | gauge | 1 | — | Memory information field AnonHugePages_bytes. |
| `node_memory_AnonPages_bytes` | gauge | 1 | — | Memory information field AnonPages_bytes. |
| `node_memory_Bounce_bytes` | gauge | 1 | — | Memory information field Bounce_bytes. |
| `node_memory_Buffers_bytes` | gauge | 1 | — | Memory information field Buffers_bytes. |
| `node_memory_Cached_bytes` | gauge | 1 | — | Memory information field Cached_bytes. |
| `node_memory_CmaFree_bytes` | gauge | 1 | — | Memory information field CmaFree_bytes. |
| `node_memory_CmaTotal_bytes` | gauge | 1 | — | Memory information field CmaTotal_bytes. |
| `node_memory_CommitLimit_bytes` | gauge | 1 | — | Memory information field CommitLimit_bytes. |
| `node_memory_Committed_AS_bytes` | gauge | 1 | — | Memory information field Committed_AS_bytes. |
| `node_memory_DirectMap1G_bytes` | gauge | 1 | — | Memory information field DirectMap1G_bytes. |
| `node_memory_DirectMap2M_bytes` | gauge | 1 | — | Memory information field DirectMap2M_bytes. |
| `node_memory_DirectMap4k_bytes` | gauge | 1 | — | Memory information field DirectMap4k_bytes. |
| `node_memory_Dirty_bytes` | gauge | 1 | — | Memory information field Dirty_bytes. |
| `node_memory_FileHugePages_bytes` | gauge | 1 | — | Memory information field FileHugePages_bytes. |
| `node_memory_FilePmdMapped_bytes` | gauge | 1 | — | Memory information field FilePmdMapped_bytes. |
| `node_memory_HardwareCorrupted_bytes` | gauge | 1 | — | Memory information field HardwareCorrupted_bytes. |
| `node_memory_HugePages_Free` | gauge | 1 | — | Memory information field HugePages_Free. |
| `node_memory_HugePages_Rsvd` | gauge | 1 | — | Memory information field HugePages_Rsvd. |
| `node_memory_HugePages_Surp` | gauge | 1 | — | Memory information field HugePages_Surp. |
| `node_memory_HugePages_Total` | gauge | 1 | — | Memory information field HugePages_Total. |
| `node_memory_Hugepagesize_bytes` | gauge | 1 | — | Memory information field Hugepagesize_bytes. |
| `node_memory_Hugetlb_bytes` | gauge | 1 | — | Memory information field Hugetlb_bytes. |
| `node_memory_Inactive_anon_bytes` | gauge | 1 | — | Memory information field Inactive_anon_bytes. |
| `node_memory_Inactive_bytes` | gauge | 1 | — | Memory information field Inactive_bytes. |
| `node_memory_Inactive_file_bytes` | gauge | 1 | — | Memory information field Inactive_file_bytes. |
| `node_memory_KReclaimable_bytes` | gauge | 1 | — | Memory information field KReclaimable_bytes. |
| `node_memory_KernelStack_bytes` | gauge | 1 | — | Memory information field KernelStack_bytes. |
| `node_memory_Mapped_bytes` | gauge | 1 | — | Memory information field Mapped_bytes. |
| `node_memory_MemAvailable_bytes` | gauge | 1 | — | Memory information field MemAvailable_bytes. |
| `node_memory_MemFree_bytes` | gauge | 1 | — | Memory information field MemFree_bytes. |
| `node_memory_MemTotal_bytes` | gauge | 1 | — | Memory information field MemTotal_bytes. |
| `node_memory_Mlocked_bytes` | gauge | 1 | — | Memory information field Mlocked_bytes. |
| `node_memory_NFS_Unstable_bytes` | gauge | 1 | — | Memory information field NFS_Unstable_bytes. |
| `node_memory_PageTables_bytes` | gauge | 1 | — | Memory information field PageTables_bytes. |
| `node_memory_Percpu_bytes` | gauge | 1 | — | Memory information field Percpu_bytes. |
| `node_memory_SReclaimable_bytes` | gauge | 1 | — | Memory information field SReclaimable_bytes. |
| `node_memory_SUnreclaim_bytes` | gauge | 1 | — | Memory information field SUnreclaim_bytes. |
| `node_memory_ShmemHugePages_bytes` | gauge | 1 | — | Memory information field ShmemHugePages_bytes. |
| `node_memory_ShmemPmdMapped_bytes` | gauge | 1 | — | Memory information field ShmemPmdMapped_bytes. |
| `node_memory_Shmem_bytes` | gauge | 1 | — | Memory information field Shmem_bytes. |
| `node_memory_Slab_bytes` | gauge | 1 | — | Memory information field Slab_bytes. |
| `node_memory_SwapCached_bytes` | gauge | 1 | — | Memory information field SwapCached_bytes. |
| `node_memory_SwapFree_bytes` | gauge | 1 | — | Memory information field SwapFree_bytes. |
| `node_memory_SwapTotal_bytes` | gauge | 1 | — | Memory information field SwapTotal_bytes. |
| `node_memory_Unevictable_bytes` | gauge | 1 | — | Memory information field Unevictable_bytes. |
| `node_memory_VmallocChunk_bytes` | gauge | 1 | — | Memory information field VmallocChunk_bytes. |
| `node_memory_VmallocTotal_bytes` | gauge | 1 | — | Memory information field VmallocTotal_bytes. |
| `node_memory_VmallocUsed_bytes` | gauge | 1 | — | Memory information field VmallocUsed_bytes. |
| `node_memory_WritebackTmp_bytes` | gauge | 1 | — | Memory information field WritebackTmp_bytes. |
| `node_memory_Writeback_bytes` | gauge | 1 | — | Memory information field Writeback_bytes. |
| `node_netstat_Icmp6_InErrors` | untyped | 1 | — | Statistic Icmp6InErrors. |
| `node_netstat_Icmp6_InMsgs` | untyped | 1 | — | Statistic Icmp6InMsgs. |
| `node_netstat_Icmp6_OutMsgs` | untyped | 1 | — | Statistic Icmp6OutMsgs. |
| `node_netstat_Icmp_InErrors` | untyped | 1 | — | Statistic IcmpInErrors. |
| `node_netstat_Icmp_InMsgs` | untyped | 1 | — | Statistic IcmpInMsgs. |
| `node_netstat_Icmp_OutMsgs` | untyped | 1 | — | Statistic IcmpOutMsgs. |
| `node_netstat_Ip6_InOctets` | untyped | 1 | — | Statistic Ip6InOctets. |
| `node_netstat_Ip6_OutOctets` | untyped | 1 | — | Statistic Ip6OutOctets. |
| `node_netstat_IpExt_InOctets` | untyped | 1 | — | Statistic IpExtInOctets. |
| `node_netstat_IpExt_OutOctets` | untyped | 1 | — | Statistic IpExtOutOctets. |
| `node_netstat_Ip_Forwarding` | untyped | 1 | — | Statistic IpForwarding. |
| `node_netstat_TcpExt_ListenDrops` | untyped | 1 | — | Statistic TcpExtListenDrops. |
| `node_netstat_TcpExt_ListenOverflows` | untyped | 1 | — | Statistic TcpExtListenOverflows. |
| `node_netstat_TcpExt_SyncookiesFailed` | untyped | 1 | — | Statistic TcpExtSyncookiesFailed. |
| `node_netstat_TcpExt_SyncookiesRecv` | untyped | 1 | — | Statistic TcpExtSyncookiesRecv. |
| `node_netstat_TcpExt_SyncookiesSent` | untyped | 1 | — | Statistic TcpExtSyncookiesSent. |
| `node_netstat_TcpExt_TCPSynRetrans` | untyped | 1 | — | Statistic TcpExtTCPSynRetrans. |
| `node_netstat_TcpExt_TCPTimeouts` | untyped | 1 | — | Statistic TcpExtTCPTimeouts. |
| `node_netstat_Tcp_ActiveOpens` | untyped | 1 | — | Statistic TcpActiveOpens. |
| `node_netstat_Tcp_CurrEstab` | untyped | 1 | — | Statistic TcpCurrEstab. |
| `node_netstat_Tcp_InErrs` | untyped | 1 | — | Statistic TcpInErrs. |
| `node_netstat_Tcp_InSegs` | untyped | 1 | — | Statistic TcpInSegs. |
| `node_netstat_Tcp_OutRsts` | untyped | 1 | — | Statistic TcpOutRsts. |
| `node_netstat_Tcp_OutSegs` | untyped | 1 | — | Statistic TcpOutSegs. |
| `node_netstat_Tcp_PassiveOpens` | untyped | 1 | — | Statistic TcpPassiveOpens. |
| `node_netstat_Tcp_RetransSegs` | untyped | 1 | — | Statistic TcpRetransSegs. |
| `node_netstat_Udp6_InDatagrams` | untyped | 1 | — | Statistic Udp6InDatagrams. |
| `node_netstat_Udp6_InErrors` | untyped | 1 | — | Statistic Udp6InErrors. |
| `node_netstat_Udp6_NoPorts` | untyped | 1 | — | Statistic Udp6NoPorts. |
| `node_netstat_Udp6_OutDatagrams` | untyped | 1 | — | Statistic Udp6OutDatagrams. |
| `node_netstat_Udp6_RcvbufErrors` | untyped | 1 | — | Statistic Udp6RcvbufErrors. |
| `node_netstat_Udp6_SndbufErrors` | untyped | 1 | — | Statistic Udp6SndbufErrors. |
| `node_netstat_UdpLite6_InErrors` | untyped | 1 | — | Statistic UdpLite6InErrors. |
| `node_netstat_UdpLite_InErrors` | untyped | 1 | — | Statistic UdpLiteInErrors. |
| `node_netstat_Udp_InDatagrams` | untyped | 1 | — | Statistic UdpInDatagrams. |
| `node_netstat_Udp_InErrors` | untyped | 1 | — | Statistic UdpInErrors. |
| `node_netstat_Udp_NoPorts` | untyped | 1 | — | Statistic UdpNoPorts. |
| `node_netstat_Udp_OutDatagrams` | untyped | 1 | — | Statistic UdpOutDatagrams. |
| `node_netstat_Udp_RcvbufErrors` | untyped | 1 | — | Statistic UdpRcvbufErrors. |
| `node_netstat_Udp_SndbufErrors` | untyped | 1 | — | Statistic UdpSndbufErrors. |
| `node_network_address_assign_type` | gauge | 7 | device | Network device property: address_assign_type |
| `node_network_carrier` | gauge | 7 | device | Network device property: carrier |
| `node_network_carrier_changes_total` | counter | 7 | device | Network device property: carrier_changes_total |
| `node_network_carrier_down_changes_total` | counter | 7 | device | Network device property: carrier_down_changes_total |
| `node_network_carrier_up_changes_total` | counter | 7 | device | Network device property: carrier_up_changes_total |
| `node_network_device_id` | gauge | 7 | device | Network device property: device_id |
| `node_network_dormant` | gauge | 7 | device | Network device property: dormant |
| `node_network_flags` | gauge | 7 | device | Network device property: flags |
| `node_network_iface_id` | gauge | 7 | device | Network device property: iface_id |
| `node_network_iface_link` | gauge | 7 | device | Network device property: iface_link |
| `node_network_iface_link_mode` | gauge | 7 | device | Network device property: iface_link_mode |
| `node_network_info` | gauge | 7 | address, adminstate, broadcast, device, duplex, ifalias, operstate | Non-numeric data from /sys/class/net/<iface>, value is always 1. |
| `node_network_mtu_bytes` | gauge | 7 | device | Network device property: mtu_bytes |
| `node_network_name_assign_type` | gauge | 4 | device | Network device property: name_assign_type |
| `node_network_net_dev_group` | gauge | 7 | device | Network device property: net_dev_group |
| `node_network_protocol_type` | gauge | 7 | device | Network device property: protocol_type |
| `node_network_receive_bytes_total` | counter | 7 | device | Network device statistic receive_bytes. |
| `node_network_receive_compressed_total` | counter | 7 | device | Network device statistic receive_compressed. |
| `node_network_receive_drop_total` | counter | 7 | device | Network device statistic receive_drop. |
| `node_network_receive_errs_total` | counter | 7 | device | Network device statistic receive_errs. |
| `node_network_receive_fifo_total` | counter | 7 | device | Network device statistic receive_fifo. |
| `node_network_receive_frame_total` | counter | 7 | device | Network device statistic receive_frame. |
| `node_network_receive_multicast_total` | counter | 7 | device | Network device statistic receive_multicast. |
| `node_network_receive_nohandler_total` | counter | 7 | device | Network device statistic receive_nohandler. |
| `node_network_receive_packets_total` | counter | 7 | device | Network device statistic receive_packets. |
| `node_network_speed_bytes` | gauge | 5 | device | Network device property: speed_bytes |
| `node_network_transmit_bytes_total` | counter | 7 | device | Network device statistic transmit_bytes. |
| `node_network_transmit_carrier_total` | counter | 7 | device | Network device statistic transmit_carrier. |
| `node_network_transmit_colls_total` | counter | 7 | device | Network device statistic transmit_colls. |
| `node_network_transmit_compressed_total` | counter | 7 | device | Network device statistic transmit_compressed. |
| `node_network_transmit_drop_total` | counter | 7 | device | Network device statistic transmit_drop. |
| `node_network_transmit_errs_total` | counter | 7 | device | Network device statistic transmit_errs. |
| `node_network_transmit_fifo_total` | counter | 7 | device | Network device statistic transmit_fifo. |
| `node_network_transmit_packets_total` | counter | 7 | device | Network device statistic transmit_packets. |
| `node_network_transmit_queue_length` | gauge | 7 | device | Network device property: transmit_queue_length |
| `node_network_up` | gauge | 7 | device | Value is 1 if operstate is 'up', 0 otherwise. |
| `node_nf_conntrack_entries` | gauge | 1 | — | Number of currently allocated flow entries for connection tracking. |
| `node_nf_conntrack_entries_limit` | gauge | 1 | — | Maximum size of connection tracking table. |
| `node_nf_conntrack_stat_drop` | gauge | 1 | — | Number of packets dropped due to conntrack failure. |
| `node_nf_conntrack_stat_early_drop` | gauge | 1 | — | Number of dropped conntrack entries to make room for new ones, if maximum table size was reached. |
| `node_nf_conntrack_stat_found` | gauge | 1 | — | Number of searched entries which were successful. |
| `node_nf_conntrack_stat_ignore` | gauge | 1 | — | Number of packets seen which are already connected to a conntrack entry. |
| `node_nf_conntrack_stat_insert` | gauge | 1 | — | Number of entries inserted into the list. |
| `node_nf_conntrack_stat_insert_failed` | gauge | 1 | — | Number of entries for which list insertion was attempted but failed. |
| `node_nf_conntrack_stat_invalid` | gauge | 1 | — | Number of packets seen which can not be tracked. |
| `node_nf_conntrack_stat_search_restart` | gauge | 1 | — | Number of conntrack table lookups which had to be restarted due to hashtable resizes. |
| `node_nfs_connections_total` | counter | 1 | — | Total number of NFSd TCP connections. |
| `node_nfs_packets_total` | counter | 2 | protocol | Total NFSd network packets (sent+received) by protocol type. |
| `node_nfs_requests_total` | counter | 99 | method, proto | Number of NFS procedures invoked. |
| `node_nfs_rpc_authentication_refreshes_total` | counter | 1 | — | Number of RPC authentication refreshes performed. |
| `node_nfs_rpc_retransmissions_total` | counter | 1 | — | Number of RPC transmissions performed. |
| `node_nfs_rpcs_total` | counter | 1 | — | Total number of RPCs performed. |
| `node_nvme_info` | gauge | 1 | device, firmware_revision, model, serial, state | Non-numeric data from /sys/class/nvme/<device>, value is always 1. |
| `node_os_info` | gauge | 1 | build_id, id, id_like, image_id, image_version, name, pretty_name, variant, variant_id, version, version_codename, version_id | A metric with a constant '1' value labeled by build_id, id, id_like, image_id, image_version, name, pretty_name, variant, variant_id, versio |
| `node_os_version` | gauge | 1 | id, id_like, name | Metric containing the major.minor part of the OS version. |
| `node_pressure_cpu_waiting_seconds_total` | counter | 1 | — | Total time in seconds that processes have waited for CPU time |
| `node_pressure_io_stalled_seconds_total` | counter | 1 | — | Total time in seconds no process could make progress due to IO congestion |
| `node_pressure_io_waiting_seconds_total` | counter | 1 | — | Total time in seconds that processes have waited due to IO congestion |
| `node_pressure_memory_stalled_seconds_total` | counter | 1 | — | Total time in seconds no process could make progress due to memory congestion |
| `node_pressure_memory_waiting_seconds_total` | counter | 1 | — | Total time in seconds that processes have waited for memory |
| `node_procs_blocked` | gauge | 1 | — | Number of processes blocked waiting for I/O to complete. |
| `node_procs_running` | gauge | 1 | — | Number of processes in runnable state. |
| `node_rapl_core_joules_total` | counter | 1 | index, path | Current RAPL core value in joules |
| `node_rapl_dram_joules_total` | counter | 1 | index, path | Current RAPL dram value in joules |
| `node_rapl_package_joules_total` | counter | 1 | index, path | Current RAPL package value in joules |
| `node_rapl_uncore_joules_total` | counter | 1 | index, path | Current RAPL uncore value in joules |
| `node_schedstat_running_seconds_total` | counter | 12 | cpu | Number of seconds CPU spent running a process. |
| `node_schedstat_timeslices_total` | counter | 12 | cpu | Number of timeslices executed by CPU. |
| `node_schedstat_waiting_seconds_total` | counter | 12 | cpu | Number of seconds spent by processing waiting for this CPU. |
| `node_scrape_collector_duration_seconds` | gauge | 45 | collector | node_exporter: Duration of a collector scrape. |
| `node_scrape_collector_success` | gauge | 45 | collector | node_exporter: Whether a collector succeeded. |
| `node_selinux_config_mode` | gauge | 1 | — | Configured SELinux enforcement mode |
| `node_selinux_current_mode` | gauge | 1 | — | Current SELinux enforcement mode |
| `node_selinux_enabled` | gauge | 1 | — | SELinux is enabled, 1 is true, 0 is false |
| `node_sockstat_FRAG6_inuse` | gauge | 1 | — | Number of FRAG6 sockets in state inuse. |
| `node_sockstat_FRAG6_memory` | gauge | 1 | — | Number of FRAG6 sockets in state memory. |
| `node_sockstat_FRAG_inuse` | gauge | 1 | — | Number of FRAG sockets in state inuse. |
| `node_sockstat_FRAG_memory` | gauge | 1 | — | Number of FRAG sockets in state memory. |
| `node_sockstat_RAW6_inuse` | gauge | 1 | — | Number of RAW6 sockets in state inuse. |
| `node_sockstat_RAW_inuse` | gauge | 1 | — | Number of RAW sockets in state inuse. |
| `node_sockstat_TCP6_inuse` | gauge | 1 | — | Number of TCP6 sockets in state inuse. |
| `node_sockstat_TCP_alloc` | gauge | 1 | — | Number of TCP sockets in state alloc. |
| `node_sockstat_TCP_inuse` | gauge | 1 | — | Number of TCP sockets in state inuse. |
| `node_sockstat_TCP_mem` | gauge | 1 | — | Number of TCP sockets in state mem. |
| `node_sockstat_TCP_mem_bytes` | gauge | 1 | — | Number of TCP sockets in state mem_bytes. |
| `node_sockstat_TCP_orphan` | gauge | 1 | — | Number of TCP sockets in state orphan. |
| `node_sockstat_TCP_tw` | gauge | 1 | — | Number of TCP sockets in state tw. |
| `node_sockstat_UDP6_inuse` | gauge | 1 | — | Number of UDP6 sockets in state inuse. |
| `node_sockstat_UDPLITE6_inuse` | gauge | 1 | — | Number of UDPLITE6 sockets in state inuse. |
| `node_sockstat_UDPLITE_inuse` | gauge | 1 | — | Number of UDPLITE sockets in state inuse. |
| `node_sockstat_UDP_inuse` | gauge | 1 | — | Number of UDP sockets in state inuse. |
| `node_sockstat_UDP_mem` | gauge | 1 | — | Number of UDP sockets in state mem. |
| `node_sockstat_UDP_mem_bytes` | gauge | 1 | — | Number of UDP sockets in state mem_bytes. |
| `node_sockstat_sockets_used` | gauge | 1 | — | Number of IPv4 sockets in use. |
| `node_softnet_backlog_len` | gauge | 12 | cpu | Softnet backlog status |
| `node_softnet_cpu_collision_total` | counter | 12 | cpu | Number of collision occur while obtaining device lock while transmitting |
| `node_softnet_dropped_total` | counter | 12 | cpu | Number of dropped packets |
| `node_softnet_flow_limit_count_total` | counter | 12 | cpu | Number of times flow limit has been reached |
| `node_softnet_processed_total` | counter | 12 | cpu | Number of processed packets |
| `node_softnet_received_rps_total` | counter | 12 | cpu | Number of times cpu woken up received_rps |
| `node_softnet_times_squeezed_total` | counter | 12 | cpu | Number of times processing packets ran out of quota |
| `node_textfile_scrape_error` | gauge | 1 | — | 1 if there was an error opening or reading a file, 0 otherwise |
| `node_thermal_zone_temp` | gauge | 2 | type, zone | Zone temperature in Celsius |
| `node_time_clocksource_available_info` | gauge | 2 | clocksource, device | Available clocksources read from '/sys/devices/system/clocksource'. |
| `node_time_clocksource_current_info` | gauge | 1 | clocksource, device | Current clocksource read from '/sys/devices/system/clocksource'. |
| `node_time_seconds` | gauge | 1 | — | System time in seconds since epoch (1970). |
| `node_time_zone_offset_seconds` | gauge | 1 | time_zone | System time zone offset in seconds. |
| `node_timex_estimated_error_seconds` | gauge | 1 | — | Estimated error in seconds. |
| `node_timex_frequency_adjustment_ratio` | gauge | 1 | — | Local clock frequency adjustment. |
| `node_timex_loop_time_constant` | gauge | 1 | — | Phase-locked loop time constant. |
| `node_timex_maxerror_seconds` | gauge | 1 | — | Maximum error in seconds. |
| `node_timex_offset_seconds` | gauge | 1 | — | Time offset in between local system and reference clock. |
| `node_timex_pps_calibration_total` | counter | 1 | — | Pulse per second count of calibration intervals. |
| `node_timex_pps_error_total` | counter | 1 | — | Pulse per second count of calibration errors. |
| `node_timex_pps_frequency_hertz` | gauge | 1 | — | Pulse per second frequency. |
| `node_timex_pps_jitter_seconds` | gauge | 1 | — | Pulse per second jitter. |
| `node_timex_pps_jitter_total` | counter | 1 | — | Pulse per second count of jitter limit exceeded events. |
| `node_timex_pps_shift_seconds` | gauge | 1 | — | Pulse per second interval duration. |
| `node_timex_pps_stability_exceeded_total` | counter | 1 | — | Pulse per second count of stability limit exceeded events. |
| `node_timex_pps_stability_hertz` | gauge | 1 | — | Pulse per second stability, average of recent frequency changes. |
| `node_timex_status` | gauge | 1 | — | Value of the status array bits. |
| `node_timex_sync_status` | gauge | 1 | — | Is clock synchronized to a reliable server (1 = yes, 0 = no). |
| `node_timex_tai_offset_seconds` | gauge | 1 | — | International Atomic Time (TAI) offset. |
| `node_timex_tick_seconds` | gauge | 1 | — | Seconds between clock ticks. |
| `node_udp_queues` | gauge | 4 | ip, queue | Number of allocated memory in the kernel for UDP datagrams in bytes. |
| `node_uname_info` | gauge | 1 | domainname, machine, nodename, release, sysname, version | Labeled system information as provided by the uname system call. |
| `node_vmstat_oom_kill` | untyped | 1 | — | /proc/vmstat information field oom_kill. |
| `node_vmstat_pgfault` | untyped | 1 | — | /proc/vmstat information field pgfault. |
| `node_vmstat_pgmajfault` | untyped | 1 | — | /proc/vmstat information field pgmajfault. |
| `node_vmstat_pgpgin` | untyped | 1 | — | /proc/vmstat information field pgpgin. |
| `node_vmstat_pgpgout` | untyped | 1 | — | /proc/vmstat information field pgpgout. |
| `node_vmstat_pswpin` | untyped | 1 | — | /proc/vmstat information field pswpin. |
| `node_vmstat_pswpout` | untyped | 1 | — | /proc/vmstat information field pswpout. |
| `node_xfs_allocation_btree_compares_total` | counter | 1 | device | Number of allocation B-tree compares for a filesystem. |
| `node_xfs_allocation_btree_lookups_total` | counter | 1 | device | Number of allocation B-tree lookups for a filesystem. |
| `node_xfs_allocation_btree_records_deleted_total` | counter | 1 | device | Number of allocation B-tree records deleted for a filesystem. |
| `node_xfs_allocation_btree_records_inserted_total` | counter | 1 | device | Number of allocation B-tree records inserted for a filesystem. |
| `node_xfs_block_map_btree_compares_total` | counter | 1 | device | Number of block map B-tree compares for a filesystem. |
| `node_xfs_block_map_btree_lookups_total` | counter | 1 | device | Number of block map B-tree lookups for a filesystem. |
| `node_xfs_block_map_btree_records_deleted_total` | counter | 1 | device | Number of block map B-tree records deleted for a filesystem. |
| `node_xfs_block_map_btree_records_inserted_total` | counter | 1 | device | Number of block map B-tree records inserted for a filesystem. |
| `node_xfs_block_mapping_extent_list_compares_total` | counter | 1 | device | Number of extent list compares for a filesystem. |
| `node_xfs_block_mapping_extent_list_deletions_total` | counter | 1 | device | Number of extent list deletions for a filesystem. |
| `node_xfs_block_mapping_extent_list_insertions_total` | counter | 1 | device | Number of extent list insertions for a filesystem. |
| `node_xfs_block_mapping_extent_list_lookups_total` | counter | 1 | device | Number of extent list lookups for a filesystem. |
| `node_xfs_block_mapping_reads_total` | counter | 1 | device | Number of block map for read operations for a filesystem. |
| `node_xfs_block_mapping_unmaps_total` | counter | 1 | device | Number of block unmaps (deletes) for a filesystem. |
| `node_xfs_block_mapping_writes_total` | counter | 1 | device | Number of block map for write operations for a filesystem. |
| `node_xfs_directory_operation_create_total` | counter | 1 | device | Number of times a new directory entry was created for a filesystem. |
| `node_xfs_directory_operation_getdents_total` | counter | 1 | device | Number of times the directory getdents operation was performed for a filesystem. |
| `node_xfs_directory_operation_lookup_total` | counter | 1 | device | Number of file name directory lookups which miss the operating systems directory name lookup cache. |
| `node_xfs_directory_operation_remove_total` | counter | 1 | device | Number of times an existing directory entry was created for a filesystem. |
| `node_xfs_extent_allocation_blocks_allocated_total` | counter | 1 | device | Number of blocks allocated for a filesystem. |
| `node_xfs_extent_allocation_blocks_freed_total` | counter | 1 | device | Number of blocks freed for a filesystem. |
| `node_xfs_extent_allocation_extents_allocated_total` | counter | 1 | device | Number of extents allocated for a filesystem. |
| `node_xfs_extent_allocation_extents_freed_total` | counter | 1 | device | Number of extents freed for a filesystem. |
| `node_xfs_inode_operation_attempts_total` | counter | 1 | device | Number of times the OS looked for an XFS inode in the inode cache. |
| `node_xfs_inode_operation_attribute_changes_total` | counter | 1 | device | Number of times the OS explicitly changed the attributes of an XFS inode. |
| `node_xfs_inode_operation_duplicates_total` | counter | 1 | device | Number of times the OS tried to add a missing XFS inode to the inode cache, but found it had already been added by another process. |
| `node_xfs_inode_operation_found_total` | counter | 1 | device | Number of times the OS looked for and found an XFS inode in the inode cache. |
| `node_xfs_inode_operation_missed_total` | counter | 1 | device | Number of times the OS looked for an XFS inode in the cache, but did not find it. |
| `node_xfs_inode_operation_reclaims_total` | counter | 1 | device | Number of times the OS reclaimed an XFS inode from the inode cache to free memory for another purpose. |
| `node_xfs_inode_operation_recycled_total` | counter | 1 | device | Number of times the OS found an XFS inode in the cache, but could not use it as it was being recycled. |
| `node_xfs_read_calls_total` | counter | 1 | device | Number of read(2) system calls made to files in a filesystem. |
| `node_xfs_vnode_active_total` | counter | 1 | device | Number of vnodes not on free lists for a filesystem. |
| `node_xfs_vnode_allocate_total` | counter | 1 | device | Number of times vn_alloc called for a filesystem. |
| `node_xfs_vnode_get_total` | counter | 1 | device | Number of times vn_get called for a filesystem. |
| `node_xfs_vnode_hold_total` | counter | 1 | device | Number of times vn_hold called for a filesystem. |
| `node_xfs_vnode_reclaim_total` | counter | 1 | device | Number of times vn_reclaim called for a filesystem. |
| `node_xfs_vnode_release_total` | counter | 1 | device | Number of times vn_rele called for a filesystem. |
| `node_xfs_vnode_remove_total` | counter | 1 | device | Number of times vn_remove called for a filesystem. |
| `node_xfs_write_calls_total` | counter | 1 | device | Number of write(2) system calls made to files in a filesystem. |
| `process_cpu_seconds_total` | counter | 1 | — | Total user and system CPU time spent in seconds. |
| `process_max_fds` | gauge | 1 | — | Maximum number of open file descriptors. |
| `process_open_fds` | gauge | 1 | — | Number of open file descriptors. |
| `process_resident_memory_bytes` | gauge | 1 | — | Resident memory size in bytes. |
| `process_start_time_seconds` | gauge | 1 | — | Start time of the process since unix epoch in seconds. |
| `process_virtual_memory_bytes` | gauge | 1 | — | Virtual memory size in bytes. |
| `process_virtual_memory_max_bytes` | gauge | 1 | — | Maximum amount of virtual memory available in bytes. |
| `promhttp_metric_handler_errors_total` | counter | 2 | cause | Total number of internal errors encountered by the promhttp metric handler. |
| `promhttp_metric_handler_requests_in_flight` | gauge | 1 | — | Current number of scrapes being served. |
| `promhttp_metric_handler_requests_total` | counter | 3 | code | Total number of scrapes by HTTP status code. |

Example raw lines:

```
# TYPE go_goroutines gauge
go_goroutines 15
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="idle"} 4.05154482e+07
# TYPE node_filesystem_avail_bytes gauge
node_filesystem_avail_bytes{device="/dev/nvme0n1p1",fstype="ext4",mountpoint="/boot"} 2.66215424e+08
# TYPE node_load1 gauge
node_load1 0.03
# TYPE node_load15 gauge
node_load15 0
# TYPE node_memory_MemTotal_bytes gauge
node_memory_MemTotal_bytes 6.73467392e+10
```

