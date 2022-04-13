FROM python:3.8-alpine

RUN apk update && apk add gcc libc-dev

COPY app /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8083

ENTRYPOINT python3 encryption.py
