# web-client

### IDE
WebStormを推奨

### プロジェクト管理
npmを使用。  
lockfileのバージョンが2であるnodeを前提としている。  

### UIコンポーネントフレームワーク
本アプリケーションはデスクトップ向けであるものとして、[Element UI](https://element.eleme.io/#/en-US) を利用する。

### Code Formatter
eslint + prettierをコミット時に自動実行。

### 開発サーバログの表示
プロジェクトルートのdocker-composeを起動して
```
docker logs flambe-web-client -f
```
