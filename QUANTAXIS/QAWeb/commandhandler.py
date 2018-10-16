
import json
import os
import shlex
import subprocess

import tornado
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler

from QUANTAXIS.QAWeb.basehandles import QABaseHandler, QAWebSocketHandler


class CommandHandler(QABaseHandler):
    def get(self):
        try:
            command = self.get_argument('command')
            # print(command)
            res = os.popen(command)
            # print(res.read())
            self.write({'result': res.read()})
        except:
            self.write({'result': 'wrong'})


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
                #print('QUANTAXIS: [{}]'.format(line))
        if p.returncode == 0:
            self.write_message('backtest run  success')

        else:
            self.write_message('Subprogram failed')
        # return p.returncode

    def on_close(self):
        pass
        # self.write_message('close')


if __name__ == "__main__":

    app = Application(
        handlers=[
            (r"/test",  CommandHandler),
        ],
        debug=True
    )
    app.listen(8011)
    tornado.ioloop.IOLoop.current().start()
