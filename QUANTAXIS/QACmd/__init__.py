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
import platform


from QUANTAXIS.QABacktest.QAAnalysis import QA_backtest_analysis_start
from QUANTAXIS.QAUtil import QA_util_log_info, QA_Setting, QA_util_mongo_initial, QA_util_mongo_make_index
from QUANTAXIS import (QA_SU_save_stock_list, QA_SU_save_stock_min, QA_SU_save_stock_xdxr,
                       QA_SU_save_stock_day, QA_SU_save_index_day, QA_SU_save_index_min,
                       QA_SU_update_stock_day)
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
        file_dir = ''

        if platform.system() == 'Windows':
            file_dir = project_dir + '\\backtest.py'
        elif platform.system() in ['Linux', 'Darwin']:
            file_dir = project_dir + '/backtest.py'

        shutil.copy(file_dir, now_path)

        QA_util_log_info(
            'Successfully generate a example strategy in :  ' + now_path)

    def help_examples(self):
        print('make a sample backtest framework')

    def do_drop_database(self, arg):
        QA_util_mongo_initial()

    def help_drop_database(self):
        print('drop quantaxis\'s databases')

    def do_make_index(self, arg):
        QA_util_mongo_make_index()

    def help_make_index(self):
        print('make index for quantaxis databases')

    def do_quit(self, arg):     # 定义quit命令所执行的操作
        sys.exit(1)

    def help_quit(self):        # 定义quit命令的帮助输出
        print("syntax: quit",)
        print("-- terminates the application")

    def do_clean(self, arg):
        try:
            if platform.system() == 'Windows':
                os.popen('del back*csv')
                os.popen('del *log')
            else:
                os.popen('rm -rf back*csv')
                os.popen('rm -rf  *log')

        except:
            pass

    def help_clean(self):
        QA_util_log_info('Clean the old backtest reports and logs')

    def do_exit(self, arg):     # 定义quit命令所执行的操作
        sys.exit(1)

    def help_exit(self):
        print('syntax: exit')
        print("-- terminates the application")

    def do_save(self, arg):
        # 仅仅是为了初始化才在这里插入用户,如果想要注册用户,要到webkit底下注册
        if arg == '':
            print("Usage: save all|insert_user|stock_day|stock_xdxr|stock_min|index_day|index_min|stock_list")
        else:
            arg = arg.split(' ')
            if len(arg)  == 1 and arg[0] == 'all':
                QA_Setting.client.quantaxis.user_list.insert(
                    {'username': 'admin', 'password': 'admin'})
                QA_SU_save_stock_day('tdx')
                QA_SU_save_stock_xdxr('tdx')
                QA_SU_save_stock_min('tdx')
                QA_SU_save_index_day('tdx')
                QA_SU_save_index_min('tdx')
                QA_SU_save_stock_list('tdx')
            else:
                for i in arg:
                    if i == 'insert_user':
                        if QA_Setting.client.quantaxis.user_list.find({'username':'admin'}).count()==0:
                            QA_Setting.client.quantaxis.user_list.insert(
                                {'username': 'admin', 'password': 'admin'})
                    else:
                        eval("QA_SU_save_%s('tdx')" %(i))

    def help_save(self):
        QA_util_log_info('Save all the stock data from pytdx')


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
