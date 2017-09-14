#coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import csv
import datetime
import json
import os
import queue
import sys
import threading
import time

import numpy as np
import pandas as pd
import pymongo
import QUANTAXIS as QA
import requests
import tushare as ts
from flask import Flask, jsonify, render_template,request,make_response
from flask_socketio import SocketIO, emit
from tabulate import tabulate

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})


@app.route("/")
def hello():
    return "QUANTAXIS SOCKET SERVER"

@app.route("/status")
def status():
    rst = make_response(jsonify('200'))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    return rst

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    return str(QA.QA_user_sign_in(request.args.get('username',''),request.args.get('password','')))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return str(QA.QA_user_sign_up(request.args.get('username',''),request.args.get('password','')))


@app.route('/query_k/<code>')
def query_k(code):
    data = json.loads(ts.get_k_data(code).to_json(orient='records'))

    return jsonify(data)


@app.route('/query/day/bfq/<code>')
def query_day_bfq(code):

    data =QA.QA_fetch_stock_day_adv(
        code, '1990-01-01', str(datetime.date.today())).to_json()
    return jsonify(data)


@app.route('/query/day/qfq/<code>')
def query_day_qfq(code):

    data =QA.QA_fetch_stock_day_adv(
        code, '1990-01-01', str(datetime.date.today())).to_qfq().to_json()
    return jsonify(data)


@app.route('/query/day/hfq/<code>')
def query_day_hfq(code):
    data =QA.QA_fetch_stock_day_adv(
        code, '1990-01-01', str(datetime.date.today())).to_hfq().to_json()
    return jsonify(data)


@app.route('/query/min/bfq/<code>')
def query_min_bfq(code):

    data =QA.QA_fetch_stock_min_adv(
        code, '2017-07-01', str(datetime.date.today()),'1min').to_json()
    return jsonify(data)
@app.route('/query/min/qfq/<code>')
def query_min_qfq(code):

    data =QA.QA_fetch_stock_min_adv(
        code, '2017-07-01', str(datetime.date.today()),'1min').to_qfq().to_json()
    return jsonify(data)


@app.route('/backtest/info', methods=['POST', 'GET'])
def query_backtest_by_():
    return jsonify(data=QA.QA_fetch_backtest_info(
            None if 'user' not in dict(list(request.args.items())) else dict(list(request.args.items()))['user'],
            None if 'cookie' not in dict(list(request.args.items())) else dict(list(request.args.items()))['cookie'],
            None if 'strategy' not in dict(list(request.args.items())) else dict(list(request.args.items()))['strategy']
            ))


@app.route('/backtest/history', methods=['POST', 'GET'])
def query_backtest_history():
    data=QA.QA_fetch_backtest_history(cookie=request.args.get('cookie',''))
    return jsonify(data)



@app.route('/backtest/info_all', methods=['POST', 'GET'])
def query_backtest():
    data=QA.QA_fetch_backtest_info()
    return jsonify(data)
def main():
    
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5050), app, handler_class=WebSocketHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()