# src/closet_search/settings/dev.py
from .base import *  # noqa
import os 

DEBUG = True
ALLOWED_HOSTS = ["*"]  # ローカル/コンテナからのアクセス許可

# DB（DockerのMySQLを使うなら環境変数で）
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
STATIC_ROOT = BASE_DIR / "staticfiles" # noqa:F405 ← BASE_DIRはbase側定義のため行単位で抑止
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/" # noqa:F405

# 便利のため（ALB等が無い前提）
USE_X_FORWARDED_HOST = False
SECURE_PROXY_SSL_HEADER = None

# CSRF はローカルで必要なら追加
# CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]
