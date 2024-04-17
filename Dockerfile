# syntax=docker/dockerfile:1

FROM python:3
WORKDIR /app
COPY . .

RUN python -m pip install -r requirements.txt
