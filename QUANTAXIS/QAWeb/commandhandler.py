
import json
import os
import shlex
import subprocess

import tornado
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler

from QUANTAXIS.QAWeb.basehandles import QABaseHandler, QAWebSocketHandler
from QUANTAXIS.QAUtil.QADict import QA_util_dict_remove_key


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


class JOBHandler(QABaseHandler):
    """job handler

    Arguments:
        QABaseHandler {[type]} -- [description]
    """

    def post(self):
        try:
            from quantaxis_run import quantaxis_run
        except:
            self.write('no quantaxis_run program on this server')
            return

        program = self.get_argument('program', 'python')
        files = self.get_argument('jobfile', False)
        if files:
            #self.wirte({'QUANTAXIS RUN': files})
            res = quantaxis_run.delay(files, program)
            self.write({'status': 'pending', 'job_id': str(res.id)})
        else:
            self.write({'status': 'error'})

            #shell_cmd = 'python "{}"'.format(shell_cmd)

    def get(self):
        try:
            from quantaxis_run.query import query_result, query_onejob
        except:
            self.write('no quantaxis_run program on this server')
            return
        job_id = self.get_argument('job_id', 'all')
        if job_id == 'all':
            self.write({'result': [QA_util_dict_remove_key(
                item, '_id') for item in query_result()]})
        else:
            self.write({'result': [QA_util_dict_remove_key(
                item, '_id') for item in query_onejob(job_id)]})


if __name__ == "__main__":

    app = Application(
        handlers=[
            (r"/test",  CommandHandler),
        ],
        debug=True
    )
    app.listen(8011)
    tornado.ioloop.IOLoop.current().start()
