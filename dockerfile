# Base build on latest Alpine Linux image
FROM alpine:latest AS build

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apk add --no-cache python3 py3-pip
RUN pip install -r requirements.txt
RUN pip install uvicorn

CMD uvicorn --host 0.0.0.0 main:app