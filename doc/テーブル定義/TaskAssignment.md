# タスクアサインテーブル定義

## task_assignment
|カラム名|型|制約|コメント|
|---|---|---|---|
|id|BIGINT UNSIGNED (20)|PK|ID|
|task_id|INT (11)|NOT NULL FK: task.id|タスクID|
|user_id|INT (11)|NOT NULL FK: user.id|ユーザID|
|created_at|DATETIME|NOT NULL|作成日時|
|updated_at|DATETIME|NOT NULL|作成日時|

- task_id, user_idの複合ユニーク制約