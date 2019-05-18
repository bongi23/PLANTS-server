#!/bin/bash

. venv/bin/activate

sudo service mongod stop
sudo service mongod start

source MONGODB='mongodb://localhost:27017/plantsDB'
source REDIS='redis://localhost:6379'

redis-server &
celery -A swagger_server.controllers.sink_controller.celery worker &

python -m swagger_server
