FROM python:3.8-slim

RUN apt-get update -y && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /todo-list

COPY test.py test.py

ENV FLASK_APP=app
CMD flask run --host=0.0.0.0 --port 5050
