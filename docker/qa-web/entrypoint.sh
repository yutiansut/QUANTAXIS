#!/bin/bash
sed -i "s|localhost|$MONGODB|" /usr/local/lib/python3.6/site-packages/QUANTAXIS/QAUtil/QASetting.py
quantaxis_webserver