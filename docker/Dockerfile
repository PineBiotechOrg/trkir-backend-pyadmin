FROM python:3.6

RUN apt-get update -y && apt-get install -y vim curl

RUN mkdir -p /app
COPY . /app

RUN cd /app && pip install -r requirements.txt
WORKDIR /app/admin


