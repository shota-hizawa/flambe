# server

## 構成

```
.
├── Dockerfile
├── alembic.ini    - alembicの設定ファイル
├── config.py      - 環境変数読み込みファイル
├── controllers    - コントローラ
├── database.py    - DBとの接続設定等
├── entities       - データエンティティの定義
├── exceptions     - 例外関連クラス
├── main.py
├── migrations     - マイグレーションファイル、設定ファイル等
├── poetry.lock
├── pyproject.toml
├── repositories   - DBのクエリ発行を担うクラス
├── schemas   　　　- Pydanticによるスキーマ定義
├── services       - サービス
└── utils          - ユーティリティ
```

## 開発環境について
### IDE
PyCharmを推奨

### プロジェクト管理
poetryを使用。  
導入については、[こちら](https://python-poetry.org/docs/) を参考にすること。

### Code Formatter
以下記事を参考に、blackをFile Watcherに追加する。  
https://qiita.com/navitime_tech/items/0a431a2d74c156d0bda2

### migrations

マイグレーションファイル生成  
※DBに既存マイグレーションが適用済みではない場合、エラーとなるので注意
```shell
docker-compose exec server bash -c "alembic revision --autogenerate"
```

マイグレーション実行
```shell
docker-compose exec server bash -c "alembic upgrade head"
```

### 開発サーバログの表示
プロジェクトルートのdocker-composeを起動して
```
docker logs flambe-server -f
```