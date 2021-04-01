FROM node:15.7.0-alpine

WORKDIR /usr/src/app

COPY package.json .
COPY package-lock.json .

RUN apk update && npm install