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
マイグレーションを実行する場合は下記の通り。  
serverのコンテナ内でalembicによってマイグレーションファイルを生成し、適用している。

```sh
docker-compose exec erver bash -c "alembic revision --autogenerate && alembic upgrade head"
```