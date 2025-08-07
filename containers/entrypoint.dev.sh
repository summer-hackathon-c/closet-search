#!/bin/bash

# DB 起動を待機（30秒以内に接続できなければ終了）
bash /wait-for-it.sh "${DB_HOST:-db}":3306 --timeout=30 --strict -- \
&& echo "✅ Database is ready"

# マイグレーション実行（失敗しても続行）
echo "🚧 Running migrations..."
python manage.py migrate || echo "⚠️ Migration failed, continuing..."

# 開発サーバー起動
echo "🚀 Starting Django development server..."
python manage.py runserver 0.0.0.0:8000