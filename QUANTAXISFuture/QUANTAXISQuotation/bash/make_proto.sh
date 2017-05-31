#!/bin/bash 
# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")
echo $SCRIPTPATH
echo 
cd $SCRIPTPATH
protoc --proto_path=../proto  --cpp_out=../lib --java_out=../lib --python_out=../lib   ../proto/stock.proto
