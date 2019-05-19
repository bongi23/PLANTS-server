FROM python:3.6-alpine

EXPOSE 8080
ADD requirements.txt ./app/
WORKDIR /app

RUN pip install -r requirements.txt

ADD . /app

CMD celery -A swagger_server.controllers.sink_controller.celery worker &

CMD python -m swagger_server