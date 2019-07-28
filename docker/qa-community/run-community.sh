#!/bin/bash

sed -i "s|localhost|$MONGODB|"  /QUANTAXIS/QUANTAXIS/QAUtil/QASetting.py
jupyter lab --allow-root &
cd ~/QADESK_BASIC && python -m http.server 80