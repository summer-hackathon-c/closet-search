# Style Log

## 📦 必要要件
Django + Docker を使った開発環境です。

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
docker compose -f docker-compose.dev.yml up --build -d
```

### 4 マイグレーション関連コマンド一覧
buildのマイグレーションでエラーが起きたら、単独で以下のマイグレーションコマンド試しても良いかもしれません。

#### 4.1 マイグレーションファイルを作成
```bash
docker compose -f docker-compose.dev.yml exec django python manage.py makemigrations
```

#### 4.2 マイグレーションを実行（テーブル作成など）
```bash
docker compose -f docker-compose.dev.yml exec django python manage.py migrate
```

#### 4.3 他ブランチで追加・変更されたマイグレーションを現在のブランチに反映する手順

1.現在のブランチで該当アプリのマイグレーションを一旦リセット
```bash
docker compose -f docker-compose.dev.yml exec django python manage.py migrate items zero
```

2.developブランチで更新されたマイグレーションファイルを取り込む
```bash
git merge develop
```

3.取り込んだマイグレーションを適用
```bash
docker compose -f docker-compose.dev.yml exec django python manage.py migrate
```

#### 4.4 マイグレーション履歴確認コマンド
```bash
docker compose -f docker-compose.dev.yml exec django python manage.py showmigrations
```

### 5.ブラウザで動作確認
以下の URL にアクセスします：

👉 http://localhost:8000

「The install worked successfully!」と表示されれば、セットアップ成功です。

### 6.Djangoプロジェクト削除

開発環境用
```bash
docker compose -f docker-compose.dev.yml down
```

### 7.コンテナ内部に入るコマンド

Django コンテナ
```bash
docker compose -f docker-compose.dev.yml exec django /bin/bash
```

MySQL コンテナ
```bash
docker compose -f docker-compose.dev.yml exec db /bin/bash
```

### 8.コンテナ内から MySQL にログイン
```bash
docker compose -f docker-compose.dev.yml exec db mysql -uapp_user -papp_pass app_db
```

### 9.Ruffコマンド

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

### 10.コンテナの状態を確認コマンド

```bash
docker compose -f docker-compose.dev.yml ps
```

### 11.ログ確認コマンド（エラーが出た時に試してください。）

Django アプリのログを確認

```bash
docker compose -f docker-compose.dev.yml logs -f django
```

MySQL コンテナのログを確認
```bash
docker compose -f docker-compose.dev.yml logs -f db
```
