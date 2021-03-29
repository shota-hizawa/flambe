# タスクテーブル定義

## task
|カラム名|型|制約|コメント|
|---|---|---|---|
|id|BIGINT UNSIGNED (20)|PK|ID|
|title|VARCHAR (255)|NOT NULL|タイトル|
|description|VARCHAR (255)||説明本文|
|status|ENUM ('TODO','DOING','DONE')|NOT NULL|ステータス|
|priority|ENUM('TODO','DOING','DONE')|NOT NULL|優先度|
|created_at|DATETIME|NOT NULL|作成日時|
|updated_at|DATETIME|NOT NULL|作成日時|