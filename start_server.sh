#!/bin/bash

. venv/bin/activate

sudo service mongod stop
sudo service mongod start

export MONGODB='mongodb://localhost:27017/plantsDB'
export REDIS='redis://localhost:6379'

redis-server &
celery -A swagger_server.controllers.sink_controller.celery worker &

python -m swagger_server
