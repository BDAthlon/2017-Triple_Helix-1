#Docker file for local building and serving only
FROM ubuntu:14.04
MAINTAINER James Scott-Brown <james@jamesscottbrown.com>

RUN useradd glyphs-user

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y git python binutils g++ make sqlite3 python-pip


RUN pip install --upgrade pip
RUN pip install gunicorn

ADD . /code
WORKDIR /code
RUN pip install -r requirements/dev.txt

USER glyphs-user
ENV FLASK_APP=/code/autoapp.py
ENV FLASK_DEBUG=1

CMD flask run --host=0.0.0.0