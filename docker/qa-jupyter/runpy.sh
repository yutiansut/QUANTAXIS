#!/bin/bash

sed -i "s|localhost|$MONGODB|"  /QUANTAXIS/QUANTAXIS/QAUtil/QASetting.py
nohup jupyter lab --allow-root &