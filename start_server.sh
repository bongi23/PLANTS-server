#!/bin/bash

. venv/bin/activate

sudo service mongod stop
sudo service mongod start

redis-server &
celery -A swagger_server.controllers.sink_controller.celery worker &

python -m swagger_server
