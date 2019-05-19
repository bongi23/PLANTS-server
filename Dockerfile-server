FROM python:3.6-alpine

EXPOSE 8080
ADD requirements.txt ./app/
WORKDIR /app

RUN pip install -r requirements.txt

ADD . /app

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]