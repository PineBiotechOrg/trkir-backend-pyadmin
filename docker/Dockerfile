FROM postgres:latest

RUN apt-get update -y && apt-get install -y vim curl tzdata
RUN apt-get install python3-pip python3-dev -y

RUN mkdir -p /app
COPY . /app

RUN cd /app && pip3 install -r requirements.txt

WORKDIR /app/admin/


