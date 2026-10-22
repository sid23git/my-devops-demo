"""
DevOps Demo Application — Production-Grade Flask API
Features:
  - Structured logging
  - Health & readiness probes (Kubernetes-ready)
  - Metrics endpoint (observability)
  - Environment-based configuration (12-Factor App)
"""
import os
import time
import logging
import platform
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from config import get_config

# ── Application Factory ────────────────────────────────────────
app = Flask(__name__)
config = get_config()

# ── Structured Logging ─────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
)
logger = logging.getLogger(config.APP_NAME)

# ── Application State (for metrics & probes) ──────────────────
APP_START_TIME = time.time()
REQUEST_COUNT = 0
_ready = True  # Toggled for readiness probe


@app.before_request
def count_requests():
    """Middleware: increment request counter for every incoming request."""
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    logger.debug("Incoming %s %s from %s", request.method, request.path, request.remote_addr)


# ── Routes ─────────────────────────────────────────────────────

@app.route("/")
def home():
    """Root endpoint — identifies the running service."""
    logger.info("Home endpoint hit")
    return jsonify({
        "message": "Hello from our CI/CD Pipeline! 🚀",
        "service": config.APP_NAME,
        "version": config.VERSION,
        "environment": config.ENVIRONMENT,
    })


@app.route("/health")
def health():
    """
    Liveness probe — tells orchestrators the process is alive.
    Returns 200 if the application process is running.
    """
    return jsonify({
        "status": "healthy",
        "version": config.VERSION,
        "uptime_seconds": round(time.time() - APP_START_TIME, 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@app.route("/ready")
def ready():
    """
    Readiness probe — tells orchestrators the app can serve traffic.
    Separated from /health so K8s can distinguish between
    'process crashed' vs 'process alive but not ready'.
    """
    if _ready:
        return jsonify({"status": "ready"}), 200
    return jsonify({"status": "not_ready"}), 503


@app.route("/metrics")
def metrics():
    """
    Observability endpoint — exposes runtime metrics.
    In production you'd use Prometheus, but this demonstrates the concept.
    """
    import sys

    # Cross-platform memory estimation
    try:
        import resource  # Unix-only
        mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    except ImportError:
        # Fallback for Windows
        mem_usage = "N/A (not available on Windows)"

    return jsonify({
        "requests_served": REQUEST_COUNT,
        "uptime_seconds": round(time.time() - APP_START_TIME, 2),
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "memory_tracked_objects": mem_usage,
        "sys_path_count": len(sys.path),
        "environment": config.ENVIRONMENT,
        "version": config.VERSION,
    })


@app.route("/info")
def info():
    """Build info endpoint — useful for verifying which version is deployed."""
    return jsonify({
        "app": config.APP_NAME,
        "version": config.VERSION,
        "environment": config.ENVIRONMENT,
        "python": platform.python_version(),
        "commit": os.getenv("GIT_COMMIT", "unknown"),
        "build_date": os.getenv("BUILD_DATE", "unknown"),
    })


# ── Application Entry Point ───────────────────────────────────

if __name__ == "__main__":
    logger.info(
        "Starting %s v%s in %s mode on %s:%s",
        config.APP_NAME, config.VERSION, config.ENVIRONMENT,
        config.HOST, config.PORT,
    )
    app.run(host=config.HOST, port=config.PORT, debug=(config.ENVIRONMENT == "development"))
