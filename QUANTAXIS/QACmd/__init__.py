# encoding: UTF-8
import cmd
import string, sys
import os,shutil
from QUANTAXIS.QAUtil import QA_util_log_info
from . import strategy_sample_simple
class CLI(cmd.Cmd):
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'QUANTAXIS> '    # 定义命令行提示符
        
    def do_version(self,arg):
        QA_util_log_info('QUANTAXIS Version 0.3.8-dev-gamma')
    def help_version(self):
        print ("syntax: version [message]",)
        print ("-- prints a version message")
    def do_makeExamples(self,arg):
        now_path=os.getcwd()
        project_dir = os.path.dirname(os.path.abspath(__file__))
        file_dir=project_dir+'\strategy_sample_simple.py'
        #print(now_path)
        #print(file_dir)
        shutil.copy(file_dir,now_path)
        QA_util_log_info('successfully generate a example strategy in'+now_path)

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