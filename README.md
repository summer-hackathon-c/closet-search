# closet-search

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

```bash
docker compose up --build -d
```

### 4.ブラウザで動作確認
以下の URL にアクセスします：

👉 http://localhost:8000

「The install worked successfully!」と表示されれば、セットアップ成功です。

### 5.Ruffコマンド

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
