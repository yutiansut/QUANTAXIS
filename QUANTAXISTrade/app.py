#!flask/bin/python
from flask import Flask, jsonify
from flask import request,make_response
from pymongo import MongoClient
import datetime
import time
from QA_trade_stock import QA_Trade_stock_api, QA_Trade_stock_util
from QA_strategy_center import strategy_loader
from QA_status_center import status_moniter

app = Flask(__name__)
st = QA_Trade_stock_api.QA_Stock()
# print(st)
db=MongoClient().quantaxis

print('*' * 6 + 'Start QUANTAXIS Trade Server' + '*' * 6)


@app.route('/', methods=['GET'])
def homepage():
    return 'Welcome to QUANTAXIS Trade Server'


@app.route('/trade/setting/config', methods=['GET'])
def get_config():
    st = QA_Trade_stock_api.QA_Stock()
    # print(st)
    configs = st.get_config()
    
    if db.trade_setting.find({'accountNo':configs['accountNo']}).count()<1:
        db.trade_setting.insert(configs)
    #print(configs)
    return jsonify(configs)


@app.route('/trade/query/cash', methods=['GET'])
def get_account_cash():
    st = QA_Trade_stock_api.QA_Stock()
    st.get_config()
    client = st.QA_trade_stock_login()
    data = st.QA_trade_stock_get_cash(client)
    return jsonify(data)


@app.route('/trade/query/stock', methods=['GET'])
def get_account_stock():
    st = QA_Trade_stock_api.QA_Stock()
    st.get_config()
    client = st.QA_trade_stock_login()
    data = st.QA_trade_stock_get_stock(client)
    return jsonify(data)
@app.route('/trade/query/assets', methods=['GET'])
def get_account_assets():
    st = QA_Trade_stock_api.QA_Stock()
    st.get_config()
    client = st.QA_trade_stock_login()
    data=QA_Trade_stock_util.QA_get_account_assest(st,client)
    rst = make_response(jsonify(data))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    return rst


@app.route('/trade/query/orders', methods=['GET'])
def get_orders():
    st = QA_Trade_stock_api.QA_Stock()
    # print(st)
    data = st.get_config()
    return jsonify(data)


@app.route('/trade/setting/congfig', methods=['POST'])
def set_config():
    if not request.json:
        abort(400)
    try:
        config['host']: request.json['host']
        config['port']: request.json['port']
        config['version']: request.json['version']
        config['branchID']: request.json['branchID']
        config['accountNo']: request.json['accountNo']
        config['tradeAccountNo']: request.json['tradeAccountNo']
        config['password']: request.json['password']
        config['txPassword']: request.json['txPassword']

        return jsonify(config), 201
    except:
        return "wrong"

"""
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_config(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get(
        'description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_config(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})
"""

if __name__ == '__main__':
    app.run(debug=True)
