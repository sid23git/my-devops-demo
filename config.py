"""
Application configuration following the 12-Factor App methodology.
All config is loaded from environment variables with sensible defaults.
"""
import os


class Config:
    """Base configuration."""
    APP_NAME = os.getenv("APP_NAME", "my-devops-demo")
    VERSION = os.getenv("APP_VERSION", "2.0.0")
    HOST = os.getenv("APP_HOST", "0.0.0.0")
    PORT = int(os.getenv("APP_PORT", 5000))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT = os.getenv("FLASK_ENV", "production")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    ENVIRONMENT = "development"


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = "WARNING"
    ENVIRONMENT = "production"


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    LOG_LEVEL = "DEBUG"
    ENVIRONMENT = "testing"


# Config selector based on FLASK_ENV
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config():
    """Return the appropriate config based on FLASK_ENV."""
    env = os.getenv("FLASK_ENV", "production")
    return config_by_name.get(env, ProductionConfig)
