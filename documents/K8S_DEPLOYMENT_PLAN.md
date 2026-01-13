# Frappe + Portal-UI Kubernetes Deployment Plan

**Target Cluster:** tkc-frappe-test (Tanzu Kubernetes)  
**Registry:** gcr.io (via Tanzu proxy)  
**Site Name:** siud.local

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Nginx Ingress Controller                     │
│                    (LoadBalancer IP)                             │
├─────────────────────────────────────────────────────────────────┤
│  /portal/*  →  portal-ui (nginx serving static Vue.js)          │
│  /*         →  frappe-frontend (nginx → backend/socketio)       │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ portal-ui    │    │frappe-frontend│   │frappe-backend│
│ (Deployment) │    │ (Deployment)  │   │ (Deployment) │
└──────────────┘    └──────────────┘    └──────────────┘
                              │                     │
                              └──────────┬──────────┘
                                         ▼
                    ┌─────────────────────────────────┐
                    │         frappe-websocket        │
                    │          (Deployment)           │
                    └─────────────────────────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────┐
        ▼                                ▼                        ▼
┌──────────────┐              ┌──────────────┐          ┌──────────────┐
│   MariaDB    │              │ Redis Cache  │          │ Redis Queue  │
│(StatefulSet) │              │ (Deployment) │          │ (Deployment) │
└──────────────┘              └──────────────┘          └──────────────┘
```

## Task Breakdown

### Task 1: Create Dockerfiles for both applications ✅
- [x] `docker/frappe/Dockerfile` - Frappe + siud app
- [x] `docker/portal-ui/Dockerfile` - Vue.js multi-stage build
- [x] `docker/portal-ui/nginx.conf` - Static files + API proxy

**Demo:** Both Dockerfiles build successfully
**Completed:** 2026-01-13

---

### Task 2: Create docker-compose for local testing ✅
- [x] `docker-compose.yml` - Full stack (Frappe + portal-ui + MariaDB + Redis)
- [x] `.env` - Configuration variables
- [x] `scripts/init-site.sh` - Init script for site creation
- [x] `docker/nginx/nginx.conf` - Reverse proxy for routing

**Demo:** `docker-compose up` runs full stack at localhost
**Completed:** 2026-01-13

---

### Task 3: Create Kubernetes base manifests
- [ ] `k8s/namespace.yaml`
- [ ] `k8s/configmap.yaml` - Frappe configuration
- [ ] `k8s/secrets.yaml` - DB passwords

**Demo:** `kubectl apply` creates namespace and configs

---

### Task 4: Create MariaDB and Redis StatefulSets/Deployments
- [ ] `k8s/mariadb.yaml` - StatefulSet + Service + PVC
- [ ] `k8s/redis.yaml` - Cache and Queue deployments + Services

**Demo:** MariaDB and Redis pods running

---

### Task 5: Create Frappe application deployments
- [ ] `k8s/frappe-backend.yaml` - Deployment + Service
- [ ] `k8s/frappe-frontend.yaml` - Deployment + Service
- [ ] `k8s/frappe-websocket.yaml` - Deployment + Service
- [ ] `k8s/frappe-workers.yaml` - Scheduler, queue-short, queue-long
- [ ] `k8s/frappe-init-job.yaml` - Site creation/migration Job
- [ ] `k8s/frappe-pvc.yaml` - Sites volume PVC

**Demo:** All Frappe pods running

---

### Task 6: Create portal-ui deployment
- [ ] `k8s/portal-ui.yaml` - Deployment + Service

**Demo:** Portal-ui pod serving static files

---

### Task 7: Create Nginx Ingress configuration
- [ ] `k8s/ingress.yaml` - Path-based routing (`/portal` → portal-ui, `/` → frappe)

**Demo:** Ingress routes traffic via LoadBalancer IP

---

### Task 8: Create Kustomization and deployment scripts
- [ ] `k8s/kustomization.yaml` - Bundle all resources
- [ ] `scripts/build-images.sh` - Build and push images
- [ ] `scripts/deploy.sh` - K8s deployment script
- [ ] `README.md` - Deployment instructions

**Demo:** Single command deploys to tkc-frappe-test

---

## Configuration Summary

| Component | Image | Port |
|-----------|-------|------|
| frappe-backend | gcr.io/PROJECT/frappe-siud:TAG | 8000 |
| frappe-frontend | gcr.io/PROJECT/frappe-siud:TAG | 8080 |
| frappe-websocket | gcr.io/PROJECT/frappe-siud:TAG | 9000 |
| portal-ui | gcr.io/PROJECT/portal-ui:TAG | 80 |
| mariadb | mariadb:11.8 | 3306 |
| redis-cache | redis:6.2-alpine | 6379 |
| redis-queue | redis:6.2-alpine | 6379 |

## Notes

- Portal-ui served at `/portal/*`, Frappe at `/*`
- MariaDB uses StatefulSet with PVC for persistence
- Frappe sites volume shared across backend/frontend/workers
- Init job runs once to create site and run migrations
