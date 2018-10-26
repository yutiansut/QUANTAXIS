
import json
import os
import shlex
import subprocess

import tornado
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler

from QUANTAXIS.QAWeb.basehandles import QABaseHandler, QAWebSocketHandler
from QUANTAXIS.QAUtil.QADict import QA_util_dict_remove_key

"""JOBHANDLER专门负责任务的部署和状态的查看

uri 路径

/job/mapper
/job/status

===

1. JOBhandler  
    - get | 查看任务的完整log
    - post | 提交任务 返回job_id
2. JOBStatusHandler
    - get | 查看job的当前状态(实时)
"""


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
            # DATABASE.joblist.insert({'program':program,'files':files,'status':'running','job_id':str(res.id)})
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



def JOBStatusHandler(QABaseHandler):
    def get(self):
        job_id = self.get_argument('job_id', 'all')