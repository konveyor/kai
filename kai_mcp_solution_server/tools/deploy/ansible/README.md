# KAI MCP Solution Server Ansible Deployment

This directory contains Ansible playbooks and roles to deploy the KAI MCP Solution Server on Kubernetes or OpenShift clusters.

## Prerequisites

- Ansible 2.9 or later
- `kubernetes.core` collection installed:
  ```bash
  ansible-galaxy collection install kubernetes.core
  ```
- `kubernetes` python package
  ```bash
  pip install kubernetes
  ```

## Deployment

### Basic Deployment

Deploy with default settings:

```bash
ansible-playbook deploy.yml
```

### Customizing the Deployment

Override default variables:

```bash
# Deploy to a specific namespace
ansible-playbook deploy.yml -e "namespace=my-namespace"

# Adjust resource limits
ansible-playbook deploy.yml -e "resources_limits_memory=1Gi"

# Use a custom image
ansible-playbook deploy.yml -e "image=quay.io/konveyor/kai-mcp-solution-server:v1.0.0"

# Use a custom storage class
ansible-playbook deploy.yml -e "storage_class=my-storage-class storage_size=2Gi"
```

### Configuration Variables

| Variable                    | Description                     | Default                                           |
| --------------------------- | ------------------------------- | ------------------------------------------------- |
| `namespace`                 | Kubernetes/OpenShift namespace  | `konveyor-kai`                                    |
| `app_name`                  | Application name                | `kai-mcp-solution-server`                         |
| `replicas`                  | Number of replicas              | `1`                                               |
| `image`                     | Container image with tag        | `quay.io/konveyor/kai-mcp-solution-server:latest` |
| `image_pull_policy`         | Image pull policy               | `Always`                                          |
| `resources_limits_cpu`      | CPU limit                       | `500m`                                            |
| `resources_limits_memory`   | Memory limit                    | `512Mi`                                           |
| `resources_requests_cpu`    | CPU request                     | `100m`                                            |
| `resources_requests_memory` | Memory request                  | `256Mi`                                           |
| `port`                      | Server port                     | `8000`                                            |
| `service_type`              | Kubernetes service type         | `ClusterIP`                                       |
| `storage_size`              | PVC storage size                | `1Gi`                                             |
| `storage_class`             | Storage class name              | `""` (cluster default)                            |
| `db_path`                   | Database path inside container  | `/data/kai_solutions.db`                          |
| `log_level`                 | Server log level                | `info`                                            |
| `host`                      | Server bind address             | `0.0.0.0`                                         |
| `route_tls_enabled`         | Enable TLS on OpenShift route   | `true`                                            |
| `route_tls_termination`     | TLS termination type            | `edge`                                            |
| `route_tls_insecure_policy` | Insecure traffic policy         | `Redirect`                                        |
| `route_host`                | Custom host for OpenShift route | `""` (auto-generated)                             |

## OpenShift vs Kubernetes

The playbook automatically detects if it's running against an OpenShift cluster by checking for the presence of the Route API. If available, it will create an OpenShift Route; otherwise, it will create a Kubernetes Ingress.

## Accessing the Server

After deployment:

- On Kubernetes: Access via the Ingress at `/kai-mcp-solution-server`
- On OpenShift: Access via the automatically created Route
