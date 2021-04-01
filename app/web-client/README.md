# web-client

### IDE
WebStormを推奨

### プロジェクト管理
npmを使用。  
lockfileのバージョンが2であるnodeを前提としている。  

### Code Formatter
eslint + prettier  
コミット時に自動実行。

### 開発サーバログの表示
プロジェクトルートのdocker-composeを起動して
```
docker logs flambe-web-client -f
```
