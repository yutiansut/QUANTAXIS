import json
import os
import shlex
import subprocess
import threading

import tornado
from QUANTAXIS.QAUtil import QA_util_log_info
from QUANTAXIS.QAUtil.QADict import QA_util_dict_remove_key
from QUANTAXIS.QAWebServer.basehandles import QABaseHandler, QAWebSocketHandler
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler


def background_task(command):
    #command = self.get_argument('command')
    cmd = shlex.split(command)
    p = subprocess.Popen(
        cmd, shell=False, close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while p.poll() is None:
        line = p.stdout.readline()
        # QA.QA_util_log_info(line)
    raise Exception


class CommandHandler(QABaseHandler):
    x = {}

    def post(self):
        print('get message')
        try:
            command = self.get_argument('command')
            # print(command)
            #command = 'bash -c "{}"'.format(command)
            print(command)

            threading.Thread(target=background_task, args=(
                command,), daemon=True).start()
            # if command not in self.x.keys():
            #     self.x[command] = background_task(command)
            # else:
            #     self.x[command].kill()
            #     self.x[command] = background_task(command)
            # print(res.read())
            self.write({'result': 'true'})
        except Exception as e:
            self.write({'result': 'wrong', 'reason': str(e)})


class CommandHandlerWS(QAWebSocketHandler):

    def on_message(self, shell_cmd):
        # shell_cmd = 'python "{}"'.format(shell_cmd)
        self.write_message({'QUANTAXIS RUN ': shell_cmd})
        cmd = shlex.split(shell_cmd)
        p = subprocess.Popen(
            cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            line = p.stdout.readline()
            line = line.strip()
            if line:
                self.write_message(line)

        if p.returncode == 0:
            self.write_message('backtest run  success')

        else:
            self.write_message('Subprogram failed')

    def on_close(self):
        pass


class RunnerHandler(QAWebSocketHandler):

    def on_message(self, shell_cmd):
        shell_cmd = 'python "{}"'.format(shell_cmd)
        self.write_message({'QUANTAXIS RUN ': shell_cmd})
        cmd = shlex.split(shell_cmd)
        p = subprocess.Popen(
            cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while p.poll() is None:
            line = p.stdout.readline()
            line = line.strip()
            if line:
                self.write_message(line)

        if p.returncode == 0:
            self.write_message('backtest run  success')

        else:
            self.write_message('Subprogram failed')

    def on_close(self):
        pass


if __name__ == "__main__":

    app = Application(
        handlers=[
            (r"/test",  CommandHandler),
        ],
        debug=True
    )
    app.listen(8011)
    tornado.ioloop.IOLoop.current().start()
