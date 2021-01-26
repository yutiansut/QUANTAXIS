#!/bin/bash
echo 'start backend & celery'
echo $MONGODB
echo $QARUN_AMQP
#cat /entrypoint.sh

quantaxis_webserver &

echo 'start celery'
celery -A quantaxis_run worker --loglevel=info
