FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /yap-api
WORKDIR /yap-api

RUN pip install pip -U
ADD requirements.txt /yap-api/
RUN pip install gunicorn && pip install --no-cache-dir -r requirements.txt

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev  -y

ADD . /yap-api