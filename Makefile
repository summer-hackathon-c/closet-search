# Ruff コマンドを実行するコンテナサービス名（docker-compose.yml の services: 名）
SERVICE=django

# コード整形（formatter）
format:
	docker compose run --rm $(SERVICE) ruff format .

# Linter 実行（自動修正あり）
lint:
	docker compose run --rm $(SERVICE) ruff check . --fix

# Linter 実行（自動修正なし）
lint-check:
	docker compose run --rm $(SERVICE) ruff check .
