#!/bin/bash
sed -i "s|localhost|$MONGODB|" /opt/conda/lib/python3.8/site-packages/QUANTAXIS/QAUtil/QASetting.py
quantaxis_webserver