#!/bin/sh
sed -i "s|localhost|$MONGODB|" /opt/conda/lib/python3.7/site-packages/QUANTAXIS/QAUtil/QASetting.py
