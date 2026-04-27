# ☸️ Kubernetes Microservice on GKE

A two-container Flask microservice deployed to **Google Kubernetes Engine (GKE)**, with infrastructure provisioned through **Terraform** and a **Cloud Build CI/CD pipeline** that builds, pushes, and deploys the containers automatically.

The application itself is small — the focus is on the deployment story: containerization, orchestration, persistent storage, infrastructure-as-code, and managed CI/CD on Google Cloud.

---

## What it does

Two Flask services share a Kubernetes Persistent Volume and work together to store and process CSV files.

**Container 1** (public-facing, port 6000):
- `POST /store-file` — Accepts a filename and CSV-style content as JSON, formats it, and writes it to the shared volume.
- `POST /calculate` — Accepts a filename and a product name, forwards the request to Container 2, and returns the result.

**Container 2** (internal, port 4000):
- `POST /processSum` — Reads the CSV file, validates the format (`product, amount`), and returns the total `amount` for the given product.

User flow:
1. Send a CSV to Container 1 → file is stored on the shared volume
2. Ask Container 1 to compute a product total → request is forwarded to Container 2 → sum is returned

---

## Architecture

```
                       ┌──────────────┐
                       │     User     │
                       └──────┬───────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │   GKE LoadBalancer     │
                  │   (Service type: LB)   │
                  └───────────┬────────────┘
                              │
                              ▼
              ┌─────────────────────────────────┐
              │         Pod (Deployment)        │
              │                                 │
              │   ┌──────────┐    ┌──────────┐  │
              │   │Container │───▶│Container │  │
              │   │    1     │    │    2     │  │
              │   │ (Flask)  │    │ (Flask)  │  │
              │   │ port 6000│    │ port 4000│  │
              │   └────┬─────┘    └────┬─────┘  │
              │        │               │        │
              │        ▼               ▼        │
              │   ┌──────────────────────────┐  │
              │   │  Persistent Volume       │  │
              │   │  /poojitha_PV_dir        │  │
              │   │  (shared CSV storage)    │  │
              │   └──────────────────────────┘  │
              └─────────────────────────────────┘
```

Both containers run inside the same pod and mount the same Persistent Volume, which is how they share files.

---

## Tech stack

- **Python 3 + Flask** — both microservices
- **Docker** — container packaging
- **Kubernetes (GKE)** — orchestration, scaling, networking
- **Terraform** — provisions the GKE cluster
- **GCP Artifact Registry** — stores Docker images
- **Cloud Build** — CI/CD pipeline (build → push → deploy)

---

## Project structure

```
.
├── Terraform Script/
│   └── Terraform.tf                  # GKE cluster definition
│
├── k8s-microservice-container1/
│   ├── container1.py                 # Flask app (file storage + routing)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── cloudbuild.yaml               # CI/CD pipeline
│   └── Manifest/
│       ├── deployment.yaml           # Pod with both containers
│       ├── service.yaml              # LoadBalancer service
│       └── persistentVolume.yaml     # Shared storage
│
└── k8s-microservice-container2/
    ├── container2.py                 # Flask app (CSV processing + sum)
    ├── Dockerfile
    ├── requirements.txt
    ├── cloudbuild.yaml               # CI/CD pipeline
    └── Manifest/
        ├── deployment.yaml
        ├── service.yaml
        └── persistentVolume.yaml
```

---

## Infrastructure setup

The Terraform script provisions a GKE cluster called `k8-cluster` in `us-central1`, spread across three zones (`a`, `b`, `c`) for higher availability. Each node uses an `e2-micro` machine type with a 20 GB standard persistent disk and Ubuntu containerd image.

```bash
cd "Terraform Script"
terraform init
terraform apply
```

---

## CI/CD pipeline

Each container has its own `cloudbuild.yaml` that runs three steps when triggered:

1. Build the Docker image
2. Push it to GCP Artifact Registry
3. Deploy it to the GKE cluster using `gke-deploy`

This means a code change → commit → automatic build, push, and rollout.

---

## API examples

**Store a file:**

```bash
curl -X POST http://<load-balancer-ip>/store-file \
  -H "Content-Type: application/json" \
  -d '{
    "file": "products.csv",
    "data": "product, amount\napple,5\napple,3\nbanana,7"
  }'
```

**Calculate sum for a product:**

```bash
curl -X POST http://<load-balancer-ip>/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "file": "products.csv",
    "product": "apple"
  }'
```

Response:

```json
{
  "file": "products.csv",
  "sum": 8
}
```

---

## Course

**CSCI 5409 — Advanced Topics in Cloud Computing**
Dalhousie University
