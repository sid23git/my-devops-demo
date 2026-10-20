# DevOps IA-II Demo — CI/CD Pipeline with GitHub Actions & Docker

## What This Project Demonstrates
A complete **CI/CD (Continuous Integration / Continuous Deployment)** pipeline that automatically:
1. Runs tests on every `git push`
2. Builds a Docker image if all tests pass
3. Pushes the image to GitHub Container Registry (GHCR)

---

## Tech Stack
| Tool | Purpose |
|---|---|
| **Flask** | Lightweight Python web framework |
| **pytest** | Automated testing |
| **Docker** | Containerize the application |
| **GitHub Actions** | CI/CD automation engine |
| **GHCR** | Docker image registry (GitHub Container Registry) |

---

## Pipeline Workflow

```
git push
    │
    ▼
┌─────────────────────┐
│  Job 1: Run Tests   │  ← Installs deps, runs pytest
└─────────┬───────────┘
          │ (only if tests pass)
          ▼
┌──────────────────────────┐
│  Job 2: Build & Push     │  ← Builds Docker image, pushes to GHCR
└──────────────────────────┘
```

---

## How to Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Run tests
pytest test_app.py -v
```

App will be available at `http://localhost:5000`

---

## Project Structure

```
my-devops-demo/
├── app.py                        # Flask web application
├── test_app.py                   # Automated tests
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container configuration
└── .github/
    └── workflows/
        └── ci.yml                # GitHub Actions pipeline
```

---

## Key DevOps Concepts Demonstrated

- **CI (Continuous Integration):** Every push triggers automated tests — bad code is caught immediately
- **CD (Continuous Delivery):** On passing tests, a Docker image is automatically built and pushed
- **Containerization:** Docker ensures the app runs identically on any machine
- **Infrastructure as Code:** The entire pipeline is defined in a YAML file, version-controlled alongside the app
- **Fail Fast:** The `needs: test` dependency means the Docker build never runs if tests fail
