FROM python:3.9

WORKDIR /code/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./teleport/requirements.txt /code/

RUN pip install -r requirements.txt

COPY ./teleport /code/
COPY ./static /static/