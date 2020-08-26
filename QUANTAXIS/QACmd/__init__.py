# encoding: UTF-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
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

from QUANTAXIS.QACmd.runner import run_backtest, run
from QUANTAXIS.QAApplication.QAAnalysis import QA_backtest_analysis_backtest
from QUANTAXIS.QAUtil import QA_util_log_info, QA_Setting, QA_util_mongo_initial
from QUANTAXIS.QASU.main import (
    QA_SU_save_bond_day,
    QA_SU_save_bond_list,
    QA_SU_save_bond_min,
    QA_SU_save_etf_day,
    QA_SU_save_etf_list,
    QA_SU_save_etf_min,
    QA_SU_save_financialfiles,
    QA_SU_save_future_day_all,
    QA_SU_save_future_day,
    QA_SU_save_future_list,
    QA_SU_save_future_min_all,
    QA_SU_save_future_min,
    QA_SU_save_index_day,
    QA_SU_save_index_list,
    QA_SU_save_index_min,
    QA_SU_save_index_transaction,
    QA_SU_save_option_300etf_day,
    QA_SU_save_option_300etf_min,
    QA_SU_save_option_50etf_day,
    QA_SU_save_option_50etf_min,
    QA_SU_save_option_commodity_day,
    QA_SU_save_option_commodity_min,
    QA_SU_save_option_contract_list,
    QA_SU_save_option_day_all,
    QA_SU_save_option_min_all,
    QA_SU_save_report_calendar_day,
    QA_SU_save_report_calendar_his,
    QA_SU_save_single_bond_day,
    QA_SU_save_single_bond_min,
    QA_SU_save_single_etf_day,
    QA_SU_save_single_etf_min,
    QA_SU_save_single_future_day,
    QA_SU_save_single_future_min,
    QA_SU_save_single_index_day,
    QA_SU_save_single_index_min,
    QA_SU_save_single_stock_day,
    QA_SU_save_single_stock_min,
    QA_SU_save_stock_block,
    QA_SU_save_stock_day,
    QA_SU_save_stock_divyield_day,
    QA_SU_save_stock_divyield_his,
    QA_SU_save_stock_info_tushare,
    QA_SU_save_stock_info,
    QA_SU_save_stock_list,
    QA_SU_save_stock_min,
    QA_SU_save_stock_transaction,
    QA_SU_save_stock_xdxr
)
from QUANTAXIS.QASU.save_binance import QA_SU_save_binance_symbol, QA_SU_save_binance_1hour, \
    QA_SU_save_binance_1day, QA_SU_save_binance_1min, QA_SU_save_binance
from QUANTAXIS.QASU.save_bitfinex import QA_SU_save_bitfinex_symbol, QA_SU_save_bitfinex_1hour, \
    QA_SU_save_bitfinex_1day, QA_SU_save_bitfinex_1min, QA_SU_save_bitfinex
from QUANTAXIS.QASU.save_bitmex import QA_SU_save_bitmex_symbol, QA_SU_save_bitmex
from QUANTAXIS.QASU.save_huobi import QA_SU_save_huobi_symbol, QA_SU_save_huobi_1hour, \
    QA_SU_save_huobi_1day, QA_SU_save_huobi_1min, QA_SU_save_huobi, QA_SU_save_huobi_realtime
from QUANTAXIS.QASU.save_okex import QA_SU_save_okex_symbol, QA_SU_save_okex_1hour, \
    QA_SU_save_okex_1day, QA_SU_save_okex_1min, QA_SU_save_okex

# 东方财富爬虫
from QUANTAXIS.QASU.main import (QA_SU_crawl_eastmoney)

from QUANTAXIS import __version__


class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'QUANTAXIS> ' # 定义命令行提示符

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

    # @click.command()
    # @click.option('--e', default=1, help='Number of greetings.')
    def do_examples(self, arg):
        QA_util_log_info('QUANTAXIS example')
        now_path = os.getcwd()
        #project_dir = os.path.dirname(os.path.abspath(__file__))

        data = requests.get(
            'https://codeload.github.com/quantaxis/QADemo/zip/master'
        )
        with open("{}{}QADEMO.zip".format(now_path, os.sep), "wb") as code:
            code.write(data.content)

        QA_util_log_info(
            'Successfully generate QADEMO in : {}, for more examples, please visit https://github.com/quantaxis/qademo'
            .format(now_path)
        )
        self.lastcmd = ''

    def help_examples(self):
        print('make a sample backtest framework')

    def do_download_updatex(self, arg):
        now_path = os.getcwd()
        data = requests.get(
            'https://raw.githubusercontent.com/QUANTAXIS/QUANTAXIS/master/config/update_x.py'
        )
        with open("{}{}update_x.py".format(now_path, os.sep), "wb") as code:
            code.write(data.content)
        self.lastcmd = ''

    def do_download_updateall(self, arg):
        now_path = os.getcwd()
        data = requests.get(
            'https://raw.githubusercontent.com/QUANTAXIS/QUANTAXIS/master/config/update_all.py'
        )
        with open("{}{}update_all.py".format(now_path, os.sep), "wb") as code:
            code.write(data.content)
        self.lastcmd = ''

    def do_drop_database(self, arg):
        QA_util_mongo_initial()
        self.lastcmd = ''

    def help_drop_database(self):
        print('drop quantaxis\'s databases')

    def do_quit(self, arg): # 定义quit命令所执行的操作
        sys.exit(1)

    def help_quit(self): # 定义quit命令的帮助输出
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
        self.lastcmd = ''

    def help_clean(self):
        QA_util_log_info('Clean the old backtest reports and logs')

    def do_exit(self, arg): # 定义quit命令所执行的操作
        sys.exit(1)

    def help_exit(self):
        print('syntax: exit')
        print("-- terminates the application")

    def print_crawl_usage(self):
        print(
            "Usage: \n\
            ----------------------------------------------------------------------------------------------------------------------\n\
            ⌨️命令格式：crawl eastmoney zjlx  6位股票代码 : 抓取 东方财富 资金流向          ❤️鸣谢❤️ www.eastmoney.com 网页提供数据！\n\
            ⌨️命令格式：crawl jrj       zjlx  6位股票代码 : 抓取 金融界   资金流向          ❤️鸣谢❤️ www.jrj.com.cn    网页提供数据！\n\
            ⌨️命令格式：crawl 10jqka    funds 6位股票代码 : 抓取 同花顺   资金流向          ❤️鸣谢❤️ www.10jqka.com.cn 网页提供数据！\n\
            -----------------------------------------------------------------------------------------------------------------------\n\
            ⌨️命令格式：crawl eastmoney zjlx  all        : 抓取 东方财富 所有股票资金流向   ❤️鸣谢❤️ www.eastmoney.com 网页提供数据！\n\
            ⌨️命令格式：crawl jrj       zjlx  all        : 抓取 金融界   所有股票资金流向   ❤️鸣谢❤️ www.jrj.com.cn    网页提供数据！\n\
            ⌨️命令格式：crawl 10jqka    funds all        : 抓取 同花顺   所有股票资金流向   ❤️鸣谢❤️ www.10jqka.com.cn 网页提供数据！\n\
            -----------------------------------------------------------------------------------------------------------------------\n\
            @yutiansut\n\
            @QUANTAXIS\n\
            请访问 https://book.yutiansut.com/\n\
            "
        )

    def do_crawl(self, arg):
        if arg == '':
            self.print_crawl_usage()
        else:
            arg = arg.split(' ')
            if len(arg) == 3 and arg[0] == 'eastmoney' and arg[
                    1] == 'zjlx' and arg[2] != 'all':
                print("  准备抓取东方财富资金流向数据 ")
                QA_SU_crawl_eastmoney(action=arg[1], stockCode=arg[2])
            elif len(arg) == 3 and arg[0] == 'jrj' and arg[
                    1] == 'zjlx' and arg[2] != 'all':
                print("❌crawl jrj zjlx XXXXXX !没有实现")
            elif len(arg) == 3 and arg[0] == '10jqka' and arg[
                    1] == 'funds' and arg[2] != 'all':
                print("❌crawl 10jqka funds XXXXXX !没有实现")
            elif len(arg) == 3 and arg[0] == 'eastmoney' and arg[
                    1] == 'zjlx' and arg[2] == 'all':
                #print("❌crawl eastmoney zjlx all !没有实现")
                print("  准备抓取东方财富资金流向数据 ")
                QA_SU_crawl_eastmoney(action=arg[1], stockCode=arg[2])

            elif len(arg) == 3 and arg[0] == 'jrj' and arg[1] == 'zjlx' and arg[
                    2] == 'all':
                print("❌crawl jrj zjlx all !没有实现")
            elif len(arg) == 3 and arg[0] == '10jqka' and arg[
                    1] == 'funds' and arg[2] == 'all':
                print("❌crawl 10jqka funds all !没有实现")
            else:
                print("❌crawl 命令格式不正确！")
                self.print_crawl_usage()
        self.lastcmd = ''

    def print_save_usage(self):
        print(
            "Usage: \n\
            命令格式：save all  : save stock_day/xdxr/ index_day/ stock_list/index_list \n\
            命令格式：save X|x  : save stock_day/xdxr/min index_day/min etf_day/min stock_list/index_list/block \n\
            命令格式：save day  : save stock_day/xdxr index_day etf_day stock_list/index_list \n\
            命令格式：save min  : save stock_min/xdxr index_min etf_min stock_list/index_list \n\
            命令格式: save future: save future_day/min/list \n\
            命令格式: save ox: save option_contract_list/option_day/option_min/option_commodity_day/option_commodity_min \n\
            命令格式: save transaction: save stock_transaction and index_transaction (Warning: Large Disk Space Required) \n\
            ------------------------------------------------------------ \n\
            命令格式：save stock_xdxr : 保存日除权除息数据 \n\
            命令格式：save stock_day  : 保存日线数据 \n\
            命令格式：save single_stock_day  : 保存单个股票日线数据 \n\
            命令格式：save stock_min  : 保存分钟线数据 \n\
            命令格式：save single_stock_min  : 保存单个股票分钟线数据 \n\
            命令格式：save index_day  : 保存指数日线数据 \n\
            命令格式：save single_index_day  : 保存单个指数日线数据 \n\
            命令格式：save index_min  : 保存指数分钟线数据 \n\
            命令格式：save single_index_min  : 保存单个指数分钟线数据 \n\
            命令格式：save future_day  : 保存期货日线数据 \n\
            命令格式：save future_day_all  : 保存期货日线数据(含合约信息,不包括已经过期摘牌的合约数据) \n\
            命令格式：save single_future_day  : 保存单个期货日线数据 \n\
            命令格式：save future_min  : 保存期货分钟线数据 \n\
            命令格式：save future_min_all  : 保存期货分钟线数据(含合约信息,不包括已经过期摘牌的合约数据) \n\
            命令格式：save single_future_min  : 保存单个期货分钟线数据 \n\
            命令格式：save etf_day    : 保存ETF日线数据 \n\
            命令格式：save single_etf_day    : 保存单个ETF日线数据 \n\
            命令格式：save etf_min    : 保存ET分钟数据 \n\
            命令格式：save stock_list : 保存股票列表 \n\
            命令格式：save stock_block: 保存板块 \n\
            命令格式：save stock_info : 保存tushare数据接口获取的股票列表 \n\
            命令格式：save financialfiles : 保存高级财务数据(自1996年开始) \n\
            命令格式：save option_contract_list 保存上市的期权合约信息（不包括已经过期摘牌的合约数据）\n\
            命令格式：save 50etf_option_day : 保存上海证券交易所50ETF期权日线数据（不包括已经过期摘牌的数据） \n\
            命令格式：save 50etf_option_min : 保存上海证券交易所50ETF期权分钟线数据（不包括已经过期摘牌的数据） \n\
            命令格式：save 300etf_option_day : 保存上海证券交易所300ETF期权日线数据（不包括已经过期摘牌的数据） \n\
            命令格式：save 300etf_option_min : 保存上海证券交易所300ETF期权分钟线数据（不包括已经过期摘牌的数据） \n\
            命令格式：save option_commodity_day : 保存商品期权日线数据（不包括已经过期摘牌的数据） \n\
            命令格式：save option_commodity_min : 保存商品期权分钟线数据（不包括已经过期摘牌的数据） \n\
            命令格式：save option_day_all : 保存上海证券交易所所有期权日线数据（不包括已经过期摘牌的数据） \n\
            命令格式：save option_min_all : 保存上海证券交易所所有期权分钟数据（不包括已经过期摘牌的数据） \n\
            命令格式：save index_list : 保存指数列表 \n\
            命令格式：save etf_list : 保存etf列表 \n\
            命令格式：save future_list : 保存期货列表 \n\
            命令格式：save bond_day  : 保存债券日线数据 \n\
            命令格式：save single_bond_day  : 保存单个债券日线数据 \n\
            命令格式：save bond_min  : 保存债券分钟线数据 \n\
            命令格式：save single_bond_min  : 保存单个债券分钟线数据 \n\
            命令格式：save bond_list : 保存债券列表 \n\
            命令格式：save bitmex : 保存bitmex交易所日线\现货交易对小时线数据 \n\
            命令格式：save binance : 保存币安交易所数据 \n\
            命令格式：save binance all : 一次性保存币安交易所日/小时/30/15/5/1分钟线数据（耗时很长） \n\
            命令格式：save binance 1day/1hour/1min : 单独保存币安交易所日/小时/分钟数据 \n\
            命令格式：save bitfinex : 保存bitfinex交易所数据 \n\
            命令格式：save bitfinex all : 一次性保存bitfinex交易所日/小时/30/15/5/1分钟线数据（耗时很长） \n\
            命令格式：save bitfinex 1day/1hour/1min : 单独保存bitfinex交易所日/小时/分钟数据 \n\
            命令格式：save huobi : 保存火币Pro交易所日/小时/分钟现货交易对数据 \n\
            命令格式：save huobi all : 一次性保存火币Pro交易所日/小时/30/15/5/1分钟线数据（耗时很长） \n\
            命令格式：save huobi 1day/1hour/1min/5min/15min/30min : 单独保存火币Pro交易所日/小时/分钟线数据 \n\
            命令格式：save huobi realtime : 接收火币Pro交易所实时行情（仅排名前30的主要币种）\n\
            命令格式：save okex : 保存OKEx交易所数据 \n\
            命令格式：save okex all : 一次性保存OKEx交易所日/小时/30/15/5/1分钟线数据（耗时很长） \n\
            命令格式：save okex 86400/3600/1800/900/300/60 : 单独保存OKEx交易所日/小时/30/15/5/1分钟数据 \n\
            ----------------------------------------------------------\n\
            if you just want to save daily data just\n\
                save all+ save stock_block+save stock_info, it about 1G data \n\
            if you want to save save the fully data including min level \n\
                save x + save stock_info \n \n\
            @yutiansut\n\
            @QUANTAXIS\n\
            请访问 https://book.yutiansut.com/\n\
            "
        )

    def do_save(self, arg):
        # 仅仅是为了初始化才在这里插入用户,如果想要注册用户,要到webkit底下注册
        if arg == '':
            self.print_save_usage()
        else:
            arg = arg.split(' ')

            if len(arg) == 1 and arg[0] == 'all':
                if QA_Setting().client.quantaxis.user_list.find(
                    {'username': 'admin'}).count() == 0:
                    QA_Setting().client.quantaxis.user_list.insert(
                        {
                            'username': 'admin',
                            'password': 'admin'
                        }
                    )
                # TODO: 将ts还是tdx作为命令传入
                # QA_SU_save_stock_day('ts')
                QA_SU_save_stock_day('tdx')
                QA_SU_save_stock_xdxr('tdx')
                # QA_SU_save_stock_min('tdx')
                QA_SU_save_index_day('tdx')
                # QA_SU_save_index_min('tdx')
                QA_SU_save_etf_list('tdx')
                # QA_SU_save_etf_day('tdx')
                # QA_SU_save_etf_min('tdx')
                QA_SU_save_index_list('tdx')
                QA_SU_save_stock_list('tdx')
                QA_SU_save_stock_block('tdx')
                # QA_SU_save_stock_info('tdx')
                # QA_SU_save_report_calendar_his()
                # QA_SU_save_stock_divyield_his()

            elif len(arg) == 1 and arg[0] == 'day':
                if QA_Setting().client.quantaxis.user_list.find(
                    {'username': 'admin'}).count() == 0:
                    QA_Setting().client.quantaxis.user_list.insert(
                        {
                            'username': 'admin',
                            'password': 'admin'
                        }
                    )
                QA_SU_save_stock_day('tdx')
                QA_SU_save_stock_xdxr('tdx')
                # QA_SU_save_stock_min('tdx')
                QA_SU_save_index_day('tdx')
                # QA_SU_save_index_min('tdx')
                QA_SU_save_etf_list('tdx')
                QA_SU_save_etf_day('tdx')
                # QA_SU_save_etf_min('tdx')
                QA_SU_save_index_list('tdx')
                QA_SU_save_stock_list('tdx')
                QA_SU_save_stock_block('tdx')
                # QA_SU_save_stock_divyield_day()
                # QA_SU_save_report_calendar_day()

            elif len(arg) == 1 and arg[0] == 'min':
                if QA_Setting().client.quantaxis.user_list.find(
                    {'username': 'admin'}).count() == 0:
                    QA_Setting().client.quantaxis.user_list.insert(
                        {
                            'username': 'admin',
                            'password': 'admin'
                        }
                    )
                # QA_SU_save_stock_day('tdx')
                QA_SU_save_stock_xdxr('tdx')
                QA_SU_save_stock_min('tdx')
                # QA_SU_save_index_day('tdx')
                QA_SU_save_index_min('tdx')
                QA_SU_save_etf_list('tdx')
                # QA_SU_save_etf_day('tdx')
                QA_SU_save_etf_min('tdx')
                QA_SU_save_stock_list('tdx')
                QA_SU_save_index_list('tdx')
                # QA_SU_save_stock_block('tdx')
            elif len(arg) == 1 and arg[0] == 'transaction':
                if QA_Setting().client.quantaxis.user_list.find(
                    {'username': 'admin'}).count() == 0:
                    QA_Setting().client.quantaxis.user_list.insert(
                        {
                            'username': 'admin',
                            'password': 'admin'
                        }
                    )
                QA_SU_save_index_transaction('tdx')
                QA_SU_save_stock_transaction('tdx')
                # QA_SU_save_stock_day('tdx')
                # QA_SU_save_stock_xdxr('tdx')
                # QA_SU_save_stock_min('tdx')
                # QA_SU_save_index_day('tdx')
                # QA_SU_save_index_min('tdx')
                # QA_SU_save_etf_list('tdx')
                # QA_SU_save_etf_day('tdx')
                # QA_SU_save_etf_min('tdx')
                # QA_SU_save_stock_list('tdx')
                # QA_SU_save_index_list('tdx')
                # QA_SU_save_stock_block('tdx')

            elif len(arg) == 1 and arg[0] in ['X', 'x']:
                if QA_Setting().client.quantaxis.user_list.find(
                    {'username': 'admin'}).count() == 0:
                    QA_Setting().client.quantaxis.user_list.insert(
                        {
                            'username': 'admin',
                            'password': 'admin'
                        }
                    )
                QA_SU_save_stock_day('tdx')
                QA_SU_save_stock_xdxr('tdx')
                QA_SU_save_stock_min('tdx')
                QA_SU_save_index_day('tdx')
                QA_SU_save_index_min('tdx')
                QA_SU_save_etf_list('tdx')
                QA_SU_save_etf_day('tdx')
                QA_SU_save_etf_min('tdx')
                QA_SU_save_stock_list('tdx')
                QA_SU_save_index_list('tdx')
                QA_SU_save_stock_block('tdx')
                QA_SU_save_future_list('tdx')
                # QA_SU_save_stock_info('tdx')
            elif len(arg) == 1 and arg[0] == "binance":
                QA_SU_save_binance_symbol()
                QA_SU_save_binance_1day()
                QA_SU_save_binance_1hour()
                QA_SU_save_binance_1min()
            elif len(arg) == 2 and arg[0] == "binance":
                if (arg[1] == 'all'):
                    QA_SU_save_binance_symbol()
                    QA_SU_save_binance_1day()
                    QA_SU_save_binance_1hour()
                    QA_SU_save_binance('30m')
                    QA_SU_save_binance('15m')
                    QA_SU_save_binance('5m')
                    QA_SU_save_binance_1min()
                else:
                    frequency = arg[1]
                    QA_SU_save_binance(frequency)
            elif len(arg) == 1 and arg[0] == "bitfinex":
                QA_SU_save_bitfinex_symbol()
                QA_SU_save_bitfinex_1day()
                QA_SU_save_bitfinex_1hour()
                QA_SU_save_bitfinex_1min()
            elif len(arg) == 2 and arg[0] == "bitfinex":
                if (arg[1] == 'all'):
                    QA_SU_save_bitfinex_symbol()
                    QA_SU_save_bitfinex_1day()
                    QA_SU_save_bitfinex_1hour()
                    QA_SU_save_bitfinex('30m')
                    QA_SU_save_bitfinex('15m')
                    QA_SU_save_bitfinex('5m')
                    QA_SU_save_bitfinex_1min()
                else:
                    frequency = arg[1]
                    QA_SU_save_bitfinex(frequency)
            elif len(arg) == 1 and arg[0] == "bitmex":
                QA_SU_save_bitmex_symbol()
                QA_SU_save_bitmex('1d')
                QA_SU_save_bitmex('1h')
                QA_SU_save_bitmex('1m')
            elif len(arg) == 1 and arg[0] == "huobi":
                QA_SU_save_huobi_symbol()
                QA_SU_save_huobi_1day()
                QA_SU_save_huobi_1hour()
                QA_SU_save_huobi_1min()
            elif len(arg) == 2 and arg[0] == "huobi":
                if (arg[1] == 'realtime'):
                    QA_SU_save_huobi_realtime()
                elif (arg[1] == 'all'):
                    QA_SU_save_huobi_symbol()
                    QA_SU_save_huobi_1day()
                    QA_SU_save_huobi_1hour()
                    QA_SU_save_huobi('30min')
                    QA_SU_save_huobi('15min')
                    QA_SU_save_huobi('5min')
                    QA_SU_save_huobi_1min()
                else:
                    frequency = arg[1]
                    QA_SU_save_huobi(frequency)
            elif len(arg) == 1 and arg[0] == "okex":
                QA_SU_save_okex_symbol()
                QA_SU_save_okex_1day()
                QA_SU_save_okex_1hour()
                QA_SU_save_okex_1min()
            elif len(arg) == 2 and arg[0] == "okex":
                if (arg[1] == 'all'):
                    QA_SU_save_okex_symbol()
                    QA_SU_save_okex_1day()
                    QA_SU_save_okex_1hour()
                    QA_SU_save_okex('1800')
                    QA_SU_save_okex('900')
                    QA_SU_save_okex('300')
                    QA_SU_save_okex_1min()
                else:
                    frequency = arg[1]
                    QA_SU_save_okex(frequency)
            elif len(arg) == 1 and arg[0] == "financialfiles":
                QA_SU_save_financialfiles()

            elif len(arg) == 1 and arg[0] == "future":
                QA_SU_save_future_day('tdx')
                QA_SU_save_future_min('tdx')
                QA_SU_save_future_list('tdx')

            elif len(arg) == 1 and arg[0] == "future_all":
                QA_SU_save_future_day_all('tdx')
                QA_SU_save_future_min_all('tdx')
                QA_SU_save_future_list('tdx')

            elif len(arg) == 1 and arg[0] == '50etf_option_day':
                QA_SU_save_option_50etf_day('tdx')

            elif len(arg) == 1 and arg[0] == '50etf_option_min':
                QA_SU_save_option_50etf_min('tdx')

            elif len(arg) == 1 and arg[0] == '300etf_option_day':
                QA_SU_save_option_300etf_day('tdx')

            elif len(arg) == 1 and arg[0] == '300etf_option_min':
                QA_SU_save_option_300etf_min('tdx')

            elif len(arg) == 1 and arg[0] == 'option_commodity_day':
                QA_SU_save_option_commodity_day('tdx')
            elif len(arg) == 1 and arg[0] == 'option_commodity_min':
                QA_SU_save_option_commodity_min('tdx')
            elif len(arg) == 1 and arg[0] in ['ox', 'OX', 'oX', 'Ox']:
                QA_SU_save_option_contract_list('tdx')
                QA_SU_save_option_50etf_day('tdx')
                QA_SU_save_option_50etf_min('tdx')
                QA_SU_save_option_300etf_day('tdx')
                QA_SU_save_option_300etf_min('tdx')
                QA_SU_save_option_commodity_day('tdx')
                QA_SU_save_option_commodity_min('tdx')
            elif len(arg) == 2 and arg[0] == 'single_stock_day':
                QA_SU_save_single_stock_day(arg[1], 'tdx')
            elif len(arg) == 2 and arg[0] == 'single_future_day':
                QA_SU_save_single_future_day(arg[1], 'tdx')
            elif len(arg) == 2 and arg[0] == 'single_index_day':
                QA_SU_save_single_index_day(arg[1], 'tdx')
            elif len(arg) == 2 and arg[0] == 'single_etf_day':
                QA_SU_save_single_etf_day(arg[1], 'tdx')
            elif len(arg) == 2 and arg[0] == 'single_stock_min':
                QA_SU_save_single_stock_min(arg[1], 'tdx')
            elif len(arg) == 2 and arg[0] == 'single_future_min':
                QA_SU_save_single_future_min(arg[1], 'tdx')
            elif len(arg) == 2 and arg[0] == 'single_index_min':
                QA_SU_save_single_index_min(arg[1], 'tdx')
            elif len(arg) == 2 and arg[0] == 'single_etf_min':
                QA_SU_save_single_etf_min(arg[1], 'tdx')
            elif len(arg) == 2 and arg[0] == 'single_bond_day':
                QA_SU_save_single_bond_day(arg[1], 'tdx')
            elif len(arg) == 2 and arg[0] == 'single_bond_min':
                QA_SU_save_single_bond_min(arg[1], 'tdx')
            else:
                for i in arg:
                    if i == 'insert_user':
                        if QA_Setting().client.quantaxis.user_list.find(
                            {'username': 'admin'}).count() == 0:
                            QA_Setting().client.quantaxis.user_list.insert(
                                {
                                    'username': 'admin',
                                    'password': 'admin'
                                }
                            )
                    else:
                        try:
                            eval("QA_SU_save_%s('tdx')" % (i))
                        except:
                            print("❌命令格式不正确！")
                            self.print_save_usage()
        self.lastcmd = ''

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
        QA_util_log_info('MORE EXAMPLE on https://github.com/QUANTAXIS/QADemo')

    def help(self):
        QA_util_log_info('fn+methods name')

    def do_ls(self, arg):
        QA_util_log_info(os.path.dirname(os.path.abspath(__file__)))


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
            shutil.copy(source, des)     # 第一个参数是文件，第二个参数目录
                                         # 若是目录
        if os.path.isdir(source):
            p, src_name = os.path.split(source)
            des = os.path.join(des, src_name)
            shutil.copytree(source, des) # 第一个参数是目录，第二个参数也是目录


# 创建CLI实例并运行


def QA_cmd():
    cli = CLI()
    cli.cmdloop()
