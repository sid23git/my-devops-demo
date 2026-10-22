# ═══════════════════════════════════════════════════════════════
#  Multi-Stage Docker Build — Production-Grade
# ═══════════════════════════════════════════════════════════════

# ── Stage 1: Builder ──────────────────────────────────────────
# Install dependencies in a temporary image to keep the final image lean
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: Runtime ──────────────────────────────────────────
# Final production image — minimal footprint
FROM python:3.11-slim AS runtime

# Metadata labels (OCI standard)
LABEL org.opencontainers.image.title="my-devops-demo" \
      org.opencontainers.image.description="DevOps CI/CD Demo Application" \
      org.opencontainers.image.source="https://github.com/sid23git/my-devops-demo"

# Security: Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY app.py config.py ./

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user (Least Privilege Principle)
USER appuser

# Expose the port Flask runs on
EXPOSE 5000

# Docker-native health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Environment variables with defaults
ENV FLASK_ENV=production \
    APP_VERSION=2.0.0 \
    LOG_LEVEL=INFO

# Run with gunicorn (production WSGI server) instead of Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "app:app"]
