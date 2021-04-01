# flambe
TODO app powered by Fast API and Vue.js

## 起動
```
docker-compose up -d
```

- `localhost:9000`
  Webクライアント
- `localhost:8000`
  APIサーバ
- `localhost:8000/docs`
  API定義（Swagger UI)
- `localhost:8000/redoc`
  API定義（Redoc）

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