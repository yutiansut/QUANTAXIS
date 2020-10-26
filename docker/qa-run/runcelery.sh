#!/bin/bash
echo 'start backend & celery'
echo $MONGODB
echo $QARUN_AMQP
#cat /entrypoint.sh

bash /entrypoint.sh &


echo 'start celery'
celery -A quantaxis_run worker --loglevel=info
