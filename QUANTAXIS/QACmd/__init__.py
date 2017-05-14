# encoding: UTF-8
import cmd
import string, sys
import os,shutil
import pymongo,csv
from QUANTAXIS.QAUtil import QA_util_log_info
from . import strategy_sample_simple
class CLI(cmd.Cmd):
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'QUANTAXIS> '    # 定义命令行提示符
        
    def do_version(self,arg):
        QA_util_log_info('QUANTAXIS Version 0.3.9-beta-dev14')
    def help_version(self):
        print ("syntax: version [message]",)
        print ("-- prints a version message")
    def do_examples(self,arg):
        QA_util_log_info('QUANTAXIS example')
        now_path=os.getcwd()
        project_dir = os.path.dirname(os.path.abspath(__file__))
        file_dir=project_dir+'\strategy_sample_simple.py'
        #print(now_path)
        #print(file_dir)
        shutil.copy(file_dir,now_path)
        QA_util_log_info('successfully generate a example strategy in'+now_path)
    def help_examples(self):
        print('make a sample backtest framework')
    def do_hello(self, arg):   # 定义hello命令所执行的操作
        QA_util_log_info ("hello "+ arg+ "!")

    def help_hello(self):        # 定义hello命令的帮助输出
        print ("syntax: hello [message]",)
        print ("-- prints a hello message")

    def do_quit(self, arg):     # 定义quit命令所执行的操作
        sys.exit(1)

    def help_quit(self):        # 定义quit命令的帮助输出
        print ("syntax: quit",)
        print ("-- terminates the application")
    def do_export(self):
        coll=pymongo.MongoClient().quantaxis.backtest_info
        coll2=pymongo.MongoClient().quantaxis.stock_info
        with open('info.csv','w',newline='') as f:
            csvwriter=csv.writer(f)
            csvwriter.writerow(['strategy','stock_list','start_time','end_time','account_cookie','total_returns','annualized_returns','benchmark_annualized_returns','win_rate','alpha','beta','sharpe','vol','benchmark_vol','max_drop','exist','outstanding','totals'])
            for item in  coll.find():
                code=item['stock_list'][0]
                try:
                    data=coll2.find_one({'code':code})
                    outstanding=data['outstanding']
                    totals=data['totals']
                    csvwriter.writerow([item['strategy'],'c'+str(item['stock_list'][0]),item['start_time'],item['end_time'],item['account_cookie'],item['total_returns'],item['annualized_returns'],item['benchmark_annualized_returns'],item['win_rate'],item['alpha'],item['beta'],item['sharpe'],item['vol'],item['benchmark_vol'],item['max_drop'],item['exist'],outstanding,totals])
                except:
                    info=sys.exc_info()  
                    print(info[0],":",info[1])
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
    #获得原始目录中所有的文件，并拼接每个文件的绝对路径
    os.chdir(src)
    src_file = [os.path.join(src, file) for file in os.listdir()]
    for source in src_file:
        #若是文件
        if os.path.isfile(source):
            shutil.copy(source, des)   #第一个参数是文件，第二个参数目录
        #若是目录
        if os.path.isdir(source):
            p, src_name = os.path.split(source)
            des = os.path.join(des, src_name)
            shutil.copytree(source, des)  #第一个参数是目录，第二个参数也是目录

# 创建CLI实例并运行

def QA_cmd():
    cli = CLI()
    cli.cmdloop()