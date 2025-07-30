# Ruff コマンドを実行するコンテナサービス名（docker-compose.yml の services: 名）
SERVICE=django

# コード整形（formatter）
format:
	docker compose -f docker-compose.dev.yml run --rm $(SERVICE) ruff format .

# Linter 実行（自動修正あり）
lint:
	docker compose -f docker-compose.dev.yml run --rm $(SERVICE) ruff check . --fix

# Linter 実行（自動修正なし）
lint-check:
	docker compose -f docker-compose.dev.yml run --rm $(SERVICE) ruff check .
