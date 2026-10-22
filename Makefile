# ─────────────────────────────────────────────────────────────
#  DevOps Demo — Developer Convenience Commands
# ─────────────────────────────────────────────────────────────

.PHONY: help install lint test test-cov security run docker-build docker-run docker-compose-up clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Setup ──────────────────────────────────────────────────
install: ## Install all dependencies (dev + prod)
	pip install -r requirements-dev.txt

# ── Quality Gates (same as CI pipeline) ────────────────────
lint: ## Run flake8 linter
	flake8 app.py config.py

test: ## Run tests with pytest
	pytest test_app.py -v

test-cov: ## Run tests with coverage report
	pytest test_app.py -v --cov=app --cov-report=term-missing --cov-fail-under=80

security: ## Run bandit security scan (SAST)
	bandit -r app.py config.py -f screen

# ── Run ────────────────────────────────────────────────────
run: ## Run the app locally
	python app.py

# ── Docker ─────────────────────────────────────────────────
docker-build: ## Build Docker image locally
	docker build -t devops-demo:latest .

docker-run: ## Run Docker container locally
	docker run -p 5000:5000 --env FLASK_ENV=production devops-demo:latest

docker-compose-up: ## Start with Docker Compose
	docker compose up --build -d

docker-compose-down: ## Stop Docker Compose
	docker compose down

# ── Cleanup ────────────────────────────────────────────────
clean: ## Remove caches and temporary files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov .coverage
