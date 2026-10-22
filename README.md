# 🚀 DevOps Demo — Production-Grade CI/CD Pipeline

[![CI/CD Pipeline](https://github.com/sid23git/my-devops-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/sid23git/my-devops-demo/actions/workflows/ci.yml)

> A fully automated **DevSecOps pipeline** demonstrating industry-standard CI/CD practices with quality gates, security scanning, matrix testing, and container vulnerability analysis.

---

## 🏗️ Architecture & Pipeline Flow

```
                          git push / PR
                              │
                              ▼
                    ┌───────────────────┐
                    │  🔍 LINT          │  Code Quality Gate
                    │  (flake8)         │  Enforces style & catches errors
                    └────────┬──────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
          ┌──────────────────┐  ┌───────────────────┐
          │  ✅ TEST (Matrix) │  │  🔒 SECURITY      │
          │  Python 3.10     │  │  SAST Scan         │
          │  Python 3.11     │  │  (bandit)          │
          │  Python 3.12     │  │                    │
          │  + Coverage ≥80% │  │                    │
          └────────┬─────────┘  └────────┬──────────┘
                   └────────┬────────────┘
                            ▼
                  ┌───────────────────┐
                  │  🐳 BUILD & PUSH  │  Multi-stage Docker build
                  │  Semantic tags    │  → GHCR
                  │  (SHA + date)     │
                  └────────┬──────────┘
                           ▼
                  ┌───────────────────┐
                  │  🛡️ CONTAINER     │  Trivy vulnerability scan
                  │  SCAN             │  Blocks CRITICAL/HIGH CVEs
                  └───────────────────┘
```

---

## 🔑 DevOps Concepts Demonstrated

| Concept | Implementation | Why It Matters |
|---|---|---|
| **CI (Continuous Integration)** | Every push runs lint + tests | Catches bugs immediately |
| **CD (Continuous Delivery)** | Auto-builds & pushes Docker images | Deployment-ready artifacts |
| **DevSecOps** | Bandit (SAST) + Trivy (container scan) | Security shifted left |
| **12-Factor App** | Config via environment variables (`config.py`) | Portable across environments |
| **Matrix Testing** | Tests across Python 3.10, 3.11, 3.12 | Ensures compatibility |
| **Test Coverage** | `pytest-cov` with ≥80% threshold | Quality enforcement |
| **Multi-stage Build** | Builder → Runtime Dockerfile | Smaller, secure images |
| **Least Privilege** | Non-root container user | Minimizes attack surface |
| **Observability** | `/health`, `/ready`, `/metrics` endpoints | Production monitoring |
| **Immutable Tags** | Semantic versioning (`SHA` + `YYYYMMDD`) | Reproducible deployments |
| **Dependency Caching** | GitHub Actions cache for pip | Faster pipeline runs |
| **Infrastructure as Code** | Pipeline defined in YAML, version-controlled | Auditable & repeatable |

---

## 📁 Project Structure

```
my-devops-demo/
├── app.py                    # Flask app — health/readiness probes, metrics, logging
├── config.py                 # 12-Factor config — environment-based settings
├── test_app.py               # 20+ tests — unit, integration, schema validation
├── requirements.txt          # Production dependencies (pinned)
├── requirements-dev.txt      # Dev/test dependencies (lint, coverage, security)
├── Dockerfile                # Multi-stage, non-root, health-checked
├── .dockerignore             # Build context optimization
├── docker-compose.yml        # Local orchestration (prod + dev profiles)
├── Makefile                  # Developer convenience commands
├── .flake8                   # Linter configuration
├── README.md                 # This file
└── .github/
    └── workflows/
        └── ci.yml            # 5-stage DevSecOps pipeline
```

---

## 🚀 Quick Start

### Run Locally

```bash
# Install all dependencies
pip install -r requirements-dev.txt

# Run the application
python app.py

# Run tests with coverage
pytest test_app.py -v --cov=app --cov-report=term-missing
```

### Run with Docker

```bash
# Build the image
docker build -t devops-demo .

# Run the container
docker run -p 5000:5000 devops-demo
```

### Run with Docker Compose

```bash
# Production mode
docker compose up --build -d

# Development mode (with hot reload)
docker compose --profile dev up --build
```

### Developer Commands (Makefile)

```bash
make help         # Show all commands
make lint         # Run linter
make test         # Run tests
make test-cov     # Tests + coverage
make security     # Run security scan
make docker-build # Build Docker image
```

---

## 🌐 API Endpoints

| Endpoint | Purpose | DevOps Concept |
|---|---|---|
| `GET /` | Service identity & version | Build metadata |
| `GET /health` | Liveness probe | Kubernetes monitoring |
| `GET /ready` | Readiness probe | Traffic management |
| `GET /metrics` | Runtime metrics | Observability |
| `GET /info` | Build info (commit, date) | Traceability |

---

## 🔒 Security Measures

1. **SAST Scanning** — Bandit analyzes Python code for security vulnerabilities
2. **Container Scanning** — Trivy scans Docker image for CVEs (blocks CRITICAL/HIGH)
3. **Non-root Container** — Application runs as unprivileged `appuser`
4. **Minimal Base Image** — `python:3.11-slim` reduces attack surface
5. **Multi-stage Build** — Build tools excluded from production image
6. **Pinned Dependencies** — Prevents supply chain attacks via version drift

---

## 🛠️ Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Flask | 3.0.0 | Python web framework |
| Gunicorn | 21.2.0 | Production WSGI server |
| pytest | 7.4.4 | Test framework |
| pytest-cov | 4.1.0 | Coverage reporting |
| flake8 | 7.0.0 | Code linting |
| bandit | 1.7.7 | SAST security scanner |
| Docker | Multi-stage | Containerization |
| Trivy | Latest | Container vulnerability scanner |
| GitHub Actions | v4 | CI/CD automation |
| GHCR | — | Container registry |

---

## 👤 Author

**Siddharth** — DevOps IA-II Demonstration  
Built with ❤️ to demonstrate production-grade CI/CD practices.
