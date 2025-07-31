# Style Log

Django + Docker を使った開発環境です。

## 📦 必要要件

- Docker
- Docker Compose

---

## 🚀 セットアップ手順

### 1. リポジトリをクローン

```bash
git clone git@github.com:summer-hackathon-c/closet-search.git
cd closet-search
```

### 2. .env を作成

.env.example を元に .env を作成します

```bash
cp .env.example .env
```

Windowsの場合は
```bash
copy .env.example .env
```

### 3.Django プロジェクトを起動

以下のコマンドでコンテナをビルド＆起動します：

開発環境用
```bash
docker compose -f docker-compose.dev.yml up --build -d
```

本番環境用
```bash
docker compose -f docker-compose.prod.yml up --build -d
```

### 3.1 初回：マイグレーション（DBテーブル作成）
```bash
docker compose -f docker-compose.dev.yml exec django python manage.py migrate
```
(実行後、docker-compose.dev.ymlの「#初回のみ〜」と記載されたコメントアウトの部分参照)


### 4.ブラウザで動作確認
以下の URL にアクセスします：

👉 http://localhost:8000

「The install worked successfully!」と表示されれば、セットアップ成功です。

### 5.Djangoプロジェクト削除

開発環境用
```bash
docker compose -f docker-compose.dev.yml down
```

本番環境用
```bash
docker compose -f docker-compose.prod.yml down
```

### 6.コンテナ内から MySQL にログイン
```bash
docker compose -f docker-compose.dev.yml exec db mysql -uapp_user -papp_pass app_db
```

### 7.Ruffコマンド

Lint(コードチェック& 自動修正)

```bash
make lint
```

Lint(コードチェックのみ)

```bash
make lint-check
```

Format（コード整形）

```bash
make format
```

### 8.ログ確認コマンド（エラーが出た時に試してください。）

Django アプリのログを確認

```bash
docker compose -f docker-compose.dev.yml logs -f django
```

MySQL コンテナのログを確認
```bash
docker compose -f docker-compose.dev.yml logs -f db
```
