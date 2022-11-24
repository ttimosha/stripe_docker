FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /stripe

WORKDIR /stripe

ADD . /stripe/

RUN pip install -r requirements.txt