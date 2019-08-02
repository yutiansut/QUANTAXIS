#!/bin/bash
sed -i "s|localhost|$MONGODB|" /QUANTAXIS/QUANTAXIS/QAUtil/QASetting.py
quantaxis_webserver