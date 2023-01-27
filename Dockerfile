FROM python:3.10-buster
ENV BOT_NAME=$BOT_NAME
ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY Pipfile /usr/src/app/"${BOT_NAME:-tg_bot}"
COPY Pipfile.lock /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system --deploy

COPY . /usr/src/app/"${BOT_NAME:-tg_bot}"
