#!/bin/sh
# wait-for-it.sh

set -e

#pip install quantaxis-servicedetect
host="$1"
shift
cmd="$@"

until qas_detect --mqhost "$EVENTMQ_IP" --mongohost "$MONGODB" do
  >&2 echo "qaservice is unavailable - sleeping"
  sleep 1
done

>&2 echo "qaservice is up - executing command"
exec $cmd