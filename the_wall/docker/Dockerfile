FROM python:3.7.3-alpine

RUN apk update && apk add build-base gcc libffi-dev

COPY thewall app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh

EXPOSE 8081

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
