#!/bin/bash

# スクリプト内でエラーが出たら即終了
set -e

# DB（MySQL）が起動して接続可能になるまで待機
# タイムアウトは30秒、接続できなければエラー終了
bash /wait-for-it.sh "${DB_HOST:-db}":3306 --timeout=30 --strict -- \
&& echo "✅ Database is ready"

# マイグレーション実行（失敗した場合はスクリプト全体が終了）
echo "🚧 Running database migrations..."
python manage.py migrate

# Gunicorn で本番サーバー起動
echo "🚀 Starting Django production server with Gunicorn..."
gunicorn closet_search.wsgi:application --bind 0.0.0.0:8000