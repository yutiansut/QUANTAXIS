#!/bin/bash

bash /entrypoint.sh &
celery -A quantaxis_run worker --loglevel=info -P eventlet