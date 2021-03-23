# ユーザテーブル定義


## user
|カラム名|型|制約|コメント|
|---|---|---|---|
|id|BIGINT UNSIGNED (20)|PK|ID|
|name|VARCHAR (255)|NOT NULL|ユーザ名|
|deleted|TINYINT (1)|NOT NULL|論理削除カラム|
|created_at|DATETIME|NOT NULL|作成日時|
|updated_at|DATETIME|NOT NULL|作成日時|