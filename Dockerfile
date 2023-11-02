
FROM python:3.10-slim-bullseye
LABEL maintainer="bindruid"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code
EXPOSE 9000
COPY Pipfile Pipfile.lock /code/

RUN apt-get update && apt-get install --no-install-recommends -y sudo

RUN groupadd --gid 1000 dev-user && \
    useradd --uid 1000 --gid dev-user --shell /bin/bash --no-create-home dev-user && \
    echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user && \
    chmod 0440 /etc/sudoers.d/dev-user && \
    mkdir -p /code/web/static && \
    mkdir -p /code/web/media && \
    chown -R dev-user:dev-user /code/web/ && \
    chmod -R 755 /code/web

RUN python -m pip install pipenv && \
    pipenv install --system --dev

USER dev-user
