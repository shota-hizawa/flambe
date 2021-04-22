# flambe
TODO app powered by Fast API and Vue.js

## 構成
```
.
├── README.md
├── app
│   ├── server     - Fast APIで実装されたAPIサーバ
│   └── web-client - Vue.jsで実装されたWebクライアント
├── db - ローカルDB用のファイル
│   ├── Dockerfile
│   ├── custom-config.cnf
│   └── initdb.d
├── doc
│   ├── 機能一覧.md
│   └── テーブル定義
├── docker-compose.yml
```

app配下の各ディレクトリには、それぞれのアプリケーションに関するREADMEが別途用意されているため各開発者は適宜参照すること。
- [app/server/README.md](app/server/README.md)
- [app/web-client/README.md](app/web-client/README.md)

## 起動
```
docker-compose up -d
```

起動時に、`app/server/migrations/versions`内にコミット済みのDBマイグレーションが`alembic`によって実行される。  
ただし、エンティティを修正・追加した場合はマイグレーションファイルの生成・適用が必要となるので[こちら](app/server/README.md#migrations)を参照すること。

- `localhost:9000`
  Webクライアント
- `localhost:8000`
  APIサーバ
- `localhost:8000/docs`
  API定義（Swagger UI)
- `localhost:8000/redoc`
  API定義（Redoc）

※API定義について、現段階ではローカル環境にてアプリケーションを起動した上でアクセスして表示する必要があるが、開発段階に応じてCI/CDを構築し最新の状態を静的ホスティングすることを想定。

## Commit Message Format
```
<prefix>: <変更内容>
```

### Prefix
原則、以下のいずれかをprefixとして指定する。
* **feat**: A new feature
* **fix**: A bug fix
* **docs**: Documentation only changes
* **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing
  semi-colons, etc)
* **refactor**: A code change that neither fixes a bug nor adds a feature
* **perf**: A code change that improves performance
* **test**: Adding missing or correcting existing tests
* **chore**: Changes to the build process or auxiliary tools and libraries such as documentation
  generation