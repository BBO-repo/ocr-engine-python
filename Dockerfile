#FROM python:3.10-slim-bullseye
FROM debian:bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libssl-dev wget git \
    python3-dev python3-pip libgtk2.0-dev \ 
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ocr-engine-python

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt