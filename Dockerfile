FROM python:3.6-slim

EXPOSE 5000
ENV PYTHONUNBUFFERED 1

# install pyenv
RUN apt-get update && \
    apt-get install -y git mercurial build-essential libssl-dev libbz2-dev zlib1g-dev libffi-dev libreadline-dev libsqlite3-dev curl && \
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

# install pipenv
RUN pip install pipenv

COPY . /app
WORKDIR /app

# instead of just pipenv install, this installs dependencies on container sytem so that we dont run a virtualenv inside a virtualenv
RUN pipenv install --system --deploy --ignore-pipfile
