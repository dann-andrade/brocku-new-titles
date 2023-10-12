# syntax=docker/dockerfile:1
FROM python:3-alpine

#Python Stuff
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN python3 -m pip install requests
RUN apk add busybox-initscripts make
RUN apk add bash
RUN apk add git

RUN mkdir app
WORKDIR /app

RUN chmod -R 755 /app

CMD /bin/sh














