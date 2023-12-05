FROM python:3.9-slim

RUN useradd -ms /bin/bash fiskal

RUN pip install pipenv

USER fiskal

WORKDIR /home/fiskal/app

ENV PIPENV_VENV_IN_PROJECT=true

CMD ["tail", "-f", "/dev/null"]