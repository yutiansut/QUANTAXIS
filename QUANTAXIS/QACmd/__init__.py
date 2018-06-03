# encoding: UTF-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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
import subprocess
import requests

from QUANTAXIS.QABacktest.QAAnalysis import QA_backtest_analysis_backtest
from QUANTAXIS.QAUtil import QA_util_log_info, QA_Setting, QA_util_mongo_initial
from QUANTAXIS.QASU.main import (QA_SU_save_stock_list, QA_SU_save_stock_min, QA_SU_save_stock_xdxr,
                       QA_SU_save_stock_block, QA_SU_save_stock_info,QA_SU_save_stock_info_tushare,
                       QA_SU_save_stock_day, QA_SU_save_index_day, QA_SU_save_index_min,
                       QA_SU_save_etf_day, QA_SU_save_etf_min)

from QUANTAXIS import __version__


class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'QUANTAXIS> '    # 定义命令行提示符

    def do_shell(self, arg):
        "run a shell commad"
        print(">", arg)
        sub_cmd = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
        print(sub_cmd.communicate()[0])

    def do_version(self, arg):
        QA_util_log_info(__version__)

    def help_version(self):
        print("syntax: version [message]",)
        print("-- prints a version message")

    #@click.command()
    #@click.option('--e', default=1, help='Number of greetings.')
    def do_examples(self, arg):
        QA_util_log_info('QUANTAXIS example')
        now_path = os.getcwd()
        #project_dir = os.path.dirname(os.path.abspath(__file__))
        
        data=requests.get('https://codeload.github.com/quantaxis/QADemo/zip/master')
        with open("{}{}QADEMO.zip".format(now_path,os.sep), "wb") as code:
            code.write(data.content)

        QA_util_log_info(
            'Successfully generate QADEMO in : {}, for more examples, please visit https://github.com/quantaxis/qademo'.format(now_path))

    def help_examples(self):
        print('make a sample backtest framework')

    def do_drop_database(self, arg):
        QA_util_mongo_initial()

    def help_drop_database(self):
        print('drop quantaxis\'s databases')

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
            print(
                "Usage: \n\
                save all  : save stock_day/xdxr/ index_day/ stock_list \n\
                save X|x  : save stock_day/xdxr/min index_day/min etf_day/min stock_list/block \n\
                save day  : save stock_day/xdxr index_day etf_day stock_list \n\
                save min  : save stock_min/xdxr index_min etf_min stock_list \n\
                ------------------------------------------------------------ \n\
                save stock_day  : save stock_day \n\
                save stock_xdxr : save stock_xdxr \n\
                save stock_min  : save stock_min \n\
                save index_day  : save index_day \n\
                save index_min  : save index_min \n\
                save etf_day    : save etf_day \n\
                save etf_min    : save etf_min \n\
                save stock_list : save stock_list \n\
                save stock_block: save stock_block \n\
                save stock_info : save stock_info \n\
                ----------------------------------------------------------\n\
                if you just want to save daily data just\n\
                    save all+ save stock_block+save stock_info, it about 1G data \n\
                if you want to save save the fully data including min level \n\
                    save x + save stock_info \n \n\
                @yutiansut\n\
                @QUANTAXIS\n\
                ")
        else:
            arg = arg.split(' ')

            if len(arg) == 1 and arg[0] == 'all':
                if QA_Setting().client.quantaxis.user_list.find({'username': 'admin'}).count() == 0:
                    QA_Setting().client.quantaxis.user_list.insert(
                        {'username': 'admin', 'password': 'admin'})
                QA_SU_save_stock_day('tdx')
                QA_SU_save_stock_xdxr('tdx')
                # QA_SU_save_stock_min('tdx')
                QA_SU_save_index_day('tdx')
                # QA_SU_save_index_min('tdx')
                # QA_SU_save_etf_day('tdx')
                # QA_SU_save_etf_min('tdx')
                QA_SU_save_stock_list('tdx')
                # QA_SU_save_stock_block('tdx')
                # QA_SU_save_stock_info('tdx')
            elif len(arg) == 1 and arg[0] == 'day':
                if QA_Setting().client.quantaxis.user_list.find({'username': 'admin'}).count() == 0:
                    QA_Setting().client.quantaxis.user_list.insert(
                        {'username': 'admin', 'password': 'admin'})
                QA_SU_save_stock_day('tdx')
                QA_SU_save_stock_xdxr('tdx')
                # QA_SU_save_stock_min('tdx')
                QA_SU_save_index_day('tdx')
                # QA_SU_save_index_min('tdx')
                QA_SU_save_etf_day('tdx')
                # QA_SU_save_etf_min('tdx')
                QA_SU_save_stock_list('tdx')
                QA_SU_save_stock_block('tdx')
            elif len(arg) == 1 and arg[0] == 'min':
                if QA_Setting().client.quantaxis.user_list.find({'username': 'admin'}).count() == 0:
                    QA_Setting().client.quantaxis.user_list.insert(
                        {'username': 'admin', 'password': 'admin'})
                # QA_SU_save_stock_day('tdx')
                QA_SU_save_stock_xdxr('tdx')
                QA_SU_save_stock_min('tdx')
                # QA_SU_save_index_day('tdx')
                QA_SU_save_index_min('tdx')
                # QA_SU_save_etf_day('tdx')
                QA_SU_save_etf_min('tdx')
                QA_SU_save_stock_list('tdx')
                # QA_SU_save_stock_block('tdx')
            elif len(arg) == 1 and arg[0] in ['X', 'x']:
                if QA_Setting().client.quantaxis.user_list.find({'username': 'admin'}).count() == 0:
                    QA_Setting().client.quantaxis.user_list.insert(
                        {'username': 'admin', 'password': 'admin'})
                QA_SU_save_stock_day('tdx')
                QA_SU_save_stock_xdxr('tdx')
                QA_SU_save_stock_min('tdx')
                QA_SU_save_index_day('tdx')
                QA_SU_save_index_min('tdx')
                QA_SU_save_etf_day('tdx')
                QA_SU_save_etf_min('tdx')
                QA_SU_save_stock_list('tdx')
                QA_SU_save_stock_block('tdx')
                # QA_SU_save_stock_info('tdx')
            else:
                for i in arg:
                    if i == 'insert_user':
                        if QA_Setting().client.quantaxis.user_list.find({'username': 'admin'}).count() == 0:
                            QA_Setting().client.quantaxis.user_list.insert(
                                {'username': 'admin', 'password': 'admin'})
                    else:


                        '''
                        save stock_day  : save stock_day 
                        save stock_xdxr : save stock_xdxr 
                        save stock_min  : save stock_min 
                        save index_day  : save index_day 
                        save index_min  : save index_min 
                        save etf_day    : save etf_day 
                        save etf_min    : save etf_min 
                        save stock_list : save stock_list
                        save stock_block: save stock_block
                        save stock_info : save stock_info
                        '''

                        try:
                            eval("QA_SU_save_%s('tdx')" % (i))
                        except:
                            print("Save Command Error ! Possible Command List is ")
                            print("save stock_day")
                            print("save stock_xdxr")
                            print("save stock_min")
                            print("save index_day")
                            print("save index_min")
                            print("save etf_day")
                            print("save etf_min")
                            print("save stock_list")
                            print("save stock_block")
                            print("save stock_info")

    def help_save(self):
        QA_util_log_info('Save all the stock data from pytdx')

    def do_fn(self, arg):
        try:
            QA_util_log_info(eval(arg))
        except:
            print(Exception)

    def do_help(self, arg):
        QA_util_log_info("Possible commands are:")
        QA_util_log_info("save")
        QA_util_log_info("clean")
        QA_util_log_info("fn")
        QA_util_log_info("drop_database")
        QA_util_log_info("examples")
        QA_util_log_info("shell")
        QA_util_log_info("version")
        QA_util_log_info("quit")
        QA_util_log_info("exit")
        QA_util_log_info('MORE EXAMPLE on https://github.com/yutiansut/QADemo')

    def help(self):
        QA_util_log_info('fn+methods name')


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
