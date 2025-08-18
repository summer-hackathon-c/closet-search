# ruff: noqa: F401, F403, F405
import os
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]  # ローカル/コンテナからのアクセス許可

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "app_db"),
        "USER": os.getenv("DB_USER", "app_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "app_pass"),
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "3306"),
    }
}

# 静的/メディアはローカル配信
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

USE_X_FORWARDED_HOST = False
SECURE_PROXY_SSL_HEADER = None
# CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]
