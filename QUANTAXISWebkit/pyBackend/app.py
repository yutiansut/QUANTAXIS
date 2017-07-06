import csv
import json
import os
import sys
import threading

import numpy as np
import pandas as pd
import pymongo
import QUANTAXIS as QA
import requests
from flask import Flask
from tabulate import tabulate

import queue

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/backtest/[cookie_id]')
def query_backtest_by_id(cookie_id):
    pass

  
if __name__ == "__main__":
  app.run(host='0.0.0.0')
