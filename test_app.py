"""
Comprehensive test suite for the DevOps Demo Application.
Covers: unit tests, endpoint validation, response schema checks.
Run with: pytest test_app.py -v --cov=app --cov-report=term-missing
"""
import pytest
from app import app


# ── Fixtures ───────────────────────────────────────────────────

@pytest.fixture
def client():
    """Create a test client with testing configuration."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Home Endpoint Tests ───────────────────────────────────────

class TestHomeEndpoint:
    """Tests for the root '/' endpoint."""

    def test_home_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_returns_json(self, client):
        response = client.get("/")
        assert response.content_type == "application/json"

    def test_home_contains_message(self, client):
        data = client.get("/").get_json()
        assert "message" in data
        assert "CI/CD Pipeline" in data["message"]

    def test_home_contains_version(self, client):
        data = client.get("/").get_json()
        assert "version" in data

    def test_home_contains_service_name(self, client):
        data = client.get("/").get_json()
        assert "service" in data

    def test_home_contains_environment(self, client):
        data = client.get("/").get_json()
        assert "environment" in data


# ── Health Endpoint Tests (Liveness Probe) ────────────────────

class TestHealthEndpoint:
    """Tests for the '/health' liveness probe."""

    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_status_is_healthy(self, client):
        data = client.get("/health").get_json()
        assert data["status"] == "healthy"

    def test_health_includes_version(self, client):
        data = client.get("/health").get_json()
        assert "version" in data

    def test_health_includes_uptime(self, client):
        data = client.get("/health").get_json()
        assert "uptime_seconds" in data
        assert isinstance(data["uptime_seconds"], (int, float))

    def test_health_includes_timestamp(self, client):
        data = client.get("/health").get_json()
        assert "timestamp" in data


# ── Readiness Endpoint Tests (Readiness Probe) ───────────────

class TestReadinessEndpoint:
    """Tests for the '/ready' readiness probe."""

    def test_ready_returns_200(self, client):
        response = client.get("/ready")
        assert response.status_code == 200

    def test_ready_status(self, client):
        data = client.get("/ready").get_json()
        assert data["status"] == "ready"


# ── Metrics Endpoint Tests (Observability) ────────────────────

class TestMetricsEndpoint:
    """Tests for the '/metrics' observability endpoint."""

    def test_metrics_returns_200(self, client):
        response = client.get("/metrics")
        assert response.status_code == 200

    def test_metrics_contains_request_count(self, client):
        data = client.get("/metrics").get_json()
        assert "requests_served" in data
        assert isinstance(data["requests_served"], int)

    def test_metrics_contains_uptime(self, client):
        data = client.get("/metrics").get_json()
        assert "uptime_seconds" in data

    def test_metrics_contains_python_version(self, client):
        data = client.get("/metrics").get_json()
        assert "python_version" in data

    def test_metrics_contains_environment(self, client):
        data = client.get("/metrics").get_json()
        assert "environment" in data


# ── Info Endpoint Tests (Build Metadata) ──────────────────────

class TestInfoEndpoint:
    """Tests for the '/info' build information endpoint."""

    def test_info_returns_200(self, client):
        response = client.get("/info")
        assert response.status_code == 200

    def test_info_contains_app_name(self, client):
        data = client.get("/info").get_json()
        assert "app" in data

    def test_info_contains_version(self, client):
        data = client.get("/info").get_json()
        assert "version" in data


# ── 404 Handling ──────────────────────────────────────────────

class TestErrorHandling:
    """Tests for error scenarios."""

    def test_unknown_route_returns_404(self, client):
        response = client.get("/nonexistent")
        assert response.status_code == 404
