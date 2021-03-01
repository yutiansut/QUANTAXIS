#!/bin/bash

sed -i "s|localhost|$MONGODB|"  /opt/conda/lib/python3.8/site-packages/QUANTAXIS/QAUtil/QASetting.py

jupyter lab --allow-root  --notebook-dir=/root --config /root/.jupyter/jupyter_notebook_config.py &
exec "$@"

cd /root/qamazing_community && python -m http.server 80
