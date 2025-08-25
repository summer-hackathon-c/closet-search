# closet_search/storage_backends.py
from django.contrib.staticfiles.storage import ManifestFilesMixin
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(ManifestFilesMixin, S3Boto3Storage):
    """
    静的ファイル:
    - ファイル名にハッシュ付与（Manifest）
    - 1年キャッシュ + immutable（CloudFrontで効く）
    - 同名上書き許可（Manifestが新名を作るのでOK）
    """
    location = "static"
    default_acl = None          # OAC運用なら private でOK
    file_overwrite = True
    custom_domain = True        # settingsの AWS_S3_CUSTOM_DOMAIN を使う
    object_parameters = {
        "CacheControl": "public, max-age=31536000, immutable"
    }


class MediaStorage(S3Boto3Storage):
    """
    メディア（ユーザーアップロードなど）:
    - 上書き防止
    - 1日キャッシュ
    """
    location = "media"
    default_acl = None
    file_overwrite = False
    custom_domain = True
    object_parameters = {
        "CacheControl": "public, max-age=86400"
    }