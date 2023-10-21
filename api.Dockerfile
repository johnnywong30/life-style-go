FROM python:3.12

COPY ./requirements-api.txt /usr/src

COPY ./requirements-shared.txt /usr/src

RUN pip3 install --upgrade pip

RUN pip3 install -r /usr/src/requirements-shared.txt

RUN pip3 install -r /usr/src/requirements-api.txt

WORKDIR /usr/src

CMD uvicorn --port $API_PORT --host 0.0.0.0 --reload app.main:app