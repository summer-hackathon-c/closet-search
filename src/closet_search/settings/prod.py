# ruff: noqa: F401, F403, F405

# src/closet_search/settings/prod.py
from .base import * # noqa
import os

DEBUG = False
ALLOWED_HOSTS = ["style-log.com", "www.style-log.com"]

# RDS: writer/reader
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.getenv("DB_PORT", "3306"),
    },
    "replica": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST_REPLICA"],
        "PORT": os.getenv("DB_PORT", "3306"),
    },
}
DATABASE_ROUTERS = ["closet_search.db_routers.PrimaryReplicaRouter"]

# S3（本番はS3配信）
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "ap-northeast-1")
AWS_S3_CUSTOM_DOMAIN = (
    f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
)
AWS_DEFAULT_ACL = None

STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
STATICFILES_STORAGE = "closet_search.storage_backends.StaticStorage"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
DEFAULT_FILE_STORAGE = "closet_search.storage_backends.MediaStorage"

# 逆プロキシ(ALB)配下
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF信頼オリジン
CSRF_TRUSTED_ORIGINS = [
    "https://style-log.com",
    "https://www.style-log.com",
]

# セキュアCookie
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
