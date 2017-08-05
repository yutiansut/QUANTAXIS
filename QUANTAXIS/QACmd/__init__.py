# encoding: UTF-8
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

import cmd
import csv
import os
import shutil
import string
import sys


from QUANTAXIS.QABacktest.QAAnalysis import QA_backtest_analysis_start
from QUANTAXIS.QAUtil import QA_util_log_info, QA_Setting
from QUANTAXIS.QABacktest.backtest_framework import backtest
from QUANTAXIS import __version__


class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'QUANTAXIS> '    # 定义命令行提示符

    def do_version(self, arg):
        QA_util_log_info(__version__)

    def help_version(self):
        print("syntax: version [message]",)
        print("-- prints a version message")

    def do_examples(self, arg):
        QA_util_log_info('QUANTAXIS example')
        now_path = os.getcwd()
        project_dir = os.path.dirname(os.path.abspath(__file__))
        #file_dir = project_dir + '\\backtest_setting.ini'
        # print(now_path)
        # print(file_dir)
        #shutil.copy(file_dir, now_path)
        file_dir = project_dir + '\\backtest.py'
        # print(now_path)
        # print(file_dir)
        shutil.copy(file_dir, now_path)

        import configparser
        config = configparser.ConfigParser()
        # set a number of parameters

        config.add_section("backtest")
        config.set("backtest", "strategy_start_date", "2017-01-01")
        config.set("backtest", "strategy_end_date", "2017-06-15")
        config.set("backtest", "strategy_gap", "6")
        config.set("backtest", "database_ip", "127.0.0.1")
        config.set("backtest", "username", "admin")
        config.set("backtest", "password", "admin")
        config.set("backtest", "strategy_name", "test_strategy")
        config.set("backtest", "benchmark_code", "hs300")
        config.set("backtest", "database_ip", "127.0.0.1")
        config.set("backtest", "database_ip", "127.0.0.1")
        config.add_section("account")
        config.set("account", "account_assets", "2530000")
        config.set("account", "stock_list", "file:csv:local")
        config.add_section("bid")
        config.set("bid", "bid_model",'market_price')
        config.add_section("strategy")
        config.set("strategy", "file_path",'file:py:local')

        
        # write to file
        config.write(open('backtest_setting.ini', "w"))


        QA_util_log_info(
            'successfully generate a example strategy in' + now_path)

    def help_examples(self):
        print('make a sample backtest framework')
    def do_backtest(self,arg):
        backtest().exec_bid()
    def help_backtest(self):
        print('next generation backtest')
    def do_hello(self, arg):   # 定义hello命令所执行的操作
        QA_util_log_info("hello " + arg + "!")

    def help_hello(self):        # 定义hello命令的帮助输出
        print("syntax: hello [message]",)
        print("-- prints a hello message")

    def do_quit(self, arg):     # 定义quit命令所执行的操作
        sys.exit(1)

    def help_quit(self):        # 定义quit命令的帮助输出
        print("syntax: quit",)
        print("-- terminates the application")

    def do_exit(self, arg):     # 定义quit命令所执行的操作
        sys.exit(1)

    def help_exit(self):
        print('syntax: exit')
        print("-- terminates the application")

    def do_performance(self, arg):
        # coding:utf-8
        # setting config
        print('now updating')
        pass

    def help_performance(self):
        print('this is a performance management which you can restart a performance test again')

    def do_export(self, arg):
        coll = QA_Setting.client.quantaxis.backtest_info
        coll2 = QA_Setting.client.quantaxis.stock_info
        with open('info.csv', 'w', newline='') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(['strategy', 'stock_list', 'start_time', 'end_time', 'account_cookie', 'total_returns', 'annualized_returns',
                                'benchmark_annualized_returns', 'win_rate', 'alpha', 'beta', 'sharpe', 'vol', 'benchmark_vol', 'max_drop', 'exist', 'outstanding', 'totals'])
            for item in coll.find():
                code = item['stock_list'][0]
                try:
                    data = coll2.find_one({'code': code})
                    outstanding = data['outstanding']
                    totals = data['totals']
                    csvwriter.writerow([item['strategy'], 'c' + str(item['stock_list'][0]), item['start_time'], item['end_time'], item['account_cookie'], item['total_returns'], item['annualized_returns'],
                                        item['benchmark_annualized_returns'], item['win_rate'], item['alpha'], item['beta'], item['sharpe'], item['vol'], item['benchmark_vol'], item['max_drop'], item['exist'], outstanding, totals])
                except:
                    info = sys.exc_info()
                    print(info[0], ":", info[1])
                    print(code)

    def help_export(self):
        print('export the backtest info to info.csv')

    # 定义quit的快捷方式


def sourcecpy(src, des):
    src = os.path.normpath(src)
    des = os.path.normpath(des)
    if not os.path.exists(src) or not os.path.exists(src):
        print("folder is not exist")
        sys.exit(1)
    # 获得原始目录中所有的文件，并拼接每个文件的绝对路径
    os.chdir(src)
    src_file = [os.path.join(src, file) for file in os.listdir()]
    for source in src_file:
        # 若是文件
        if os.path.isfile(source):
            shutil.copy(source, des)  # 第一个参数是文件，第二个参数目录
        # 若是目录
        if os.path.isdir(source):
            p, src_name = os.path.split(source)
            des = os.path.join(des, src_name)
            shutil.copytree(source, des)  # 第一个参数是目录，第二个参数也是目录

# 创建CLI实例并运行


def QA_cmd():
    cli = CLI()
    cli.cmdloop()
