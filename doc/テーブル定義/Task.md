# タスクテーブル定義

## task
|カラム名|型|制約|コメント|
|---|---|---|---|
|id|BIGINT UNSIGNED (20)|PK|ID|
|title|VARCHAR (255)|NOT NULL|タイトル|
|description|VARCHAR (255)||説明本文|
|status|VARCHAR (10)|NOT NULL|ステータス|
|priority|VARCHAR (10)|NOT NULL|優先度|
|deleted|TINYINT (1)|NOT NULL|論理削除カラム|
|created_at|DATETIME|NOT NULL|作成日時|
|updated_at|DATETIME|NOT NULL|作成日時|