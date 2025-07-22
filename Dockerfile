FROM python:3.12-alpine

WORKDIR /code

COPY ./requirements.txt /

RUN pip install --root-user-action=ignore --upgrade pip
RUN pip install --root-user-action=ignore -r /requirements.txt

COPY . /code