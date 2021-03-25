# ユーザテーブル定義


## user
|カラム名|型|制約|コメント|
|---|---|---|---|
|id|BIGINT UNSIGNED (20)|PK|ID|
|username|VARCHAR (255)|NOT NULL UNIQUE|ユーザ名|
|password_hash|VARCHAR (128)|NOT NULL|パスワードのSHA256ハッシュ値。|
|deleted|TINYINT (1)|NOT NULL|論理削除カラム|
|created_at|DATETIME|NOT NULL|作成日時|
|updated_at|DATETIME|NOT NULL|作成日時|

※初回リリースにおいては、論理削除されているユーザも含めて同一名は許容されない仕様とする