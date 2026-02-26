"""Environment-driven application configuration."""

import os


PRODUCT_NAME = os.getenv("PRODUCT_NAME", "Bridgaton AI")
PRODUCT_TAGLINE = os.getenv("PRODUCT_TAGLINE", "AI Inventory & Demand Intelligence Engine")
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
API_VERSION = os.getenv("API_VERSION", "1.0.0")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

API_KEY = os.getenv("API_KEY", "change-me")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
