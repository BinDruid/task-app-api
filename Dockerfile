
FROM python:3.10-slim-bullseye
LABEL maintainer="bindruid"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code
EXPOSE 9000
COPY Pipfile Pipfile.lock /code/

RUN groupadd --gid 1000 dev-user && \
    useradd --uid 1000 --gid dev-user --no-create-home dev-user

RUN python -m pip install pipenv && \
    pipenv install --system --dev

USER dev-user