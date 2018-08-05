#!/bin/sh
#MONGO_HOME=/root/usr/mongo
#MONGO_BIN=${MONGO_HOME}/bin
#MONGO_LOG=${MONGO_HOME}/log
#MONGO_DATA=${MONGO_HOME}/data
#MONGO_CONF=${MONGO_HOME}/conf

MONGO_BIN_MONGOD=${MONGO_BIN}/mongod
#MONGO_CONF_MONGOD=${MONGO_CONF}/mongod.ini
MONGO_LOG_MONGOD=${MONGO_LOG}/mongodb.log
MONGO_BIN_MONGO=${MONGO_BIN}/mongo

start()
{
    tmp=`ps -ef | grep ${MONGO_BIN_MONGOD} | wc -l`if [ $tmp -gt 1 ]; then
      echo "The server arealdy started...abort!"
      exit 1
    fi
    deleteLock
    cd ${MONGO_BIN}
    ${MONGO_BIN_MONGOD} --dbpath ${MONGO_DATA} --port 27017 --fork --logpath ${MONGOD_LOG_MONGOD} --logappend
    echo "Start MongoDB server in ${MONGO_BIN_MONGOD} OK!"
}

stop()
{
    cd ${MONGO_BIN}
    ${MONGO_BIN_MONGO} admin --eval "db.shutdownServer()"
    echo "Stopped MongoDB server"
}

usage()
{
        echo "Usage: $0 [start|stop|restart]"
}

deleteLock()
{
    echo "Deleting mongod.lock"
    cd ${MONGO_DATA}
    /bin/rm -f mongod.lock
    echo "Delete mongod.lock OK!"
}

if [ $# -lt 1 ];then
        usage
        exit
fi

if [ "$1" = "start" ];then
        start

elif [ "$1" = "stop" ];then
        stop

elif [ "$1" = "restart" ];then
        stop
        start

else
        usage
fi