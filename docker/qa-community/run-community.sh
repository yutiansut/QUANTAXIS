#!/bin/bash

sed -i "s|localhost|$MONGODB|"  /usr/local/lib/python3.6/site-packages/QUANTAXIS/QAUtil/QASetting.py
jupyter lab --allow-root  --notebook-dir=~ &
cd ~/QADESK_BASIC && python -m http.server 80