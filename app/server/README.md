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
```shell
docker-compose exec server bash -c "alembic revision --autogenerate"
```

マイグレーション実行
```shell
docker-compose exec server bash -c "alembic upgrade head"
```