import cmd
import string, sys
from .QACommand import QA_Command_make_cfg
from QUANTAXIS.QAUtil import QA_util_log_info

class CLI(cmd.Cmd):
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'QUANTAXIS> '    # 定义命令行提示符
        
    def do_version(self,arg):
        QA_util_log_info('QUANTAXIS Version 0.3.8-dev-gamma')
    def help_version(self):
        print ("syntax: version [message]",)
        print ("-- prints a version message")

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
    do_q = do_quit

# 创建CLI实例并运行
cli = CLI()
cli.cmdloop()