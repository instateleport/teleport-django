FROM python:3.9

WORKDIR /code/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/