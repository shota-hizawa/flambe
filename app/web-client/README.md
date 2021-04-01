# web-client

## 構成
```
.
├── Dockerfile
├── babel.config.js
├── package-lock.json
├── package.json
├── public
│   ├── favicon.ico
│   └── index.html
├── src
│   ├── App.vue
│   ├── api         - APIのリクエスト・レスポンス定義、呼び出し処理等
│   ├── assets
│   ├── components  - 各種コンポーネント
│   ├── main.ts     - エントリポイント
│   ├── models
│   ├── router
│   ├── styles      - グローバルスタイル
│   ├── type.d.ts
│   ├── utils       - ユーティリティ
│   └── views       - 各画面と対応するコンポーネント
├── tsconfig.json
└── vue.config.js
```

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
