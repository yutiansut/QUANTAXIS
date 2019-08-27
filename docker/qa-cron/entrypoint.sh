#!/bin/bash
set -e

sed -i "s|localhost|$MONGODB|" /usr/local/lib/python3.6/site-packages/QUANTAXIS/QAUtil/QASetting.py
exec "$@"
