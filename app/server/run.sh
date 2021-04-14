#!/bin/bash

echo "Waiting for mysql to start..."
until mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" &> /dev/null
do
    sleep 1
done

alembic upgrade head
uvicorn main:app --reload --port=8000 --host=0.0.0.0