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
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from tabulate import tabulate

import queue

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)



@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})



@app.route("/")
def hello():
    return "Hello World!"


@app.route('/backtest/[cookie_id]')
def query_backtest_by_id(cookie_id):
    pass

  
def main():
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
