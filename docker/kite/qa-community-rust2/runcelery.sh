#!/bin/bash
echo 'start backend & celery'
echo $MONGODB
echo $QARUN_AMQP
#cat /entrypoint.sh

quantaxis_webserver &
qifi_manager &
qavifiserver &
/root/portfoliohandler &

echo 'start quantaxis_run job worker'
celery -A quantaxis_run worker --loglevel=info
