FROM python:3.9-slim as builder

WORKDIR /usr/src/app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt > requirements.txt


FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/requirements.txt .

RUN apt-get update && \
    apt-get -y install gcc libmariadb-dev && \
    apt-get -y install default-mysql-client

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0" ]
