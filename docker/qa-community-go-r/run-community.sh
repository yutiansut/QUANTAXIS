#!/bin/bash

sed -i "s|localhost|$MONGODB|"  /opt/conda/lib/python3.7/site-packages/QUANTAXIS/QAUtil/QASetting.py
jupyter lab --allow-root  --notebook-dir=~ --config /root/.jupyter/jupyter_notebook_config.py &
cd /root/QADESK_BASIC && python -m http.server 80