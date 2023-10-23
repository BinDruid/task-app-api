
FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
EXPOSE 9000
COPY Pipfile Pipfile.lock /code/
RUN python -m pip install pipenv && pipenv install --system --dev