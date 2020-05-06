FROM python:3.7-alpine

RUN apk add gcc musl-dev linux-headers postgresql-dev busybox-extras && rm -rf /var/cache/apk/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY chat/ chat/

COPY *.py ./

EXPOSE 8000/tcp

