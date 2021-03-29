# ユーザテーブル定義


## user
|カラム名|型|制約|コメント|
|---|---|---|---|
|id|INT (11)|PK|ID|
|username|VARCHAR (255)|NOT NULL UNIQUE|ユーザ名|
|password_hash|VARCHAR (128)|NOT NULL|パスワードのSHA256ハッシュ値。|
|created_at|DATETIME|NOT NULL|作成日時|
|updated_at|DATETIME|NOT NULL|作成日時|
