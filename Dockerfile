FROM python:3.12-alpine

WORKDIR /code

COPY ./requirements.txt /
RUN pip install -r /requirements.txt
COPY . /code