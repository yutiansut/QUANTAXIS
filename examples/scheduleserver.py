import datetime

from QUANTAXIS.QAWebServer.schedulehandler import *
from QUANTAXIS.QAWebServer.server import start_server

def task(job_id):
    print('fin', job_id, datetime.datetime.now())
    if job_id == 1:
        print('xx1')
    elif job_id == '111':
        print('xx1')
    else:
        print('known job', job_id)


scheduler = init_scheduler()


class ScheduleForRunning(QASchedulerHandler):

    """
    添加:  get http://0.0.0.0:2225/scheduler/map?action=add&job_id=11&interval=2
    查询所有任务: get http://0.0.0.0:2225/scheduler/query
    """

    def get(self):
        jobid = self.get_argument('jobid', 1)
        action = self.get_argument('action', 'addinterval')
        running_interval = self.get_argument('interval', 3)
        hour = int(self.get_argument('hour', 3))
        minute = int(self.get_argument('minute', 3))
        second = int(self.get_argument('second', 3))
        if action == 'addinterval':
            scheduler.add_job(task, 'interval',
                              seconds=running_interval, id=jobid, args=(jobid,))
        elif action == 'addcron':
            """
            http://0.0.0.0:2225/scheduler/map?action=addcron&hour=4&minute=21&second=0&jobid=z1
            """
            scheduler.add_job(task, 'cron', hour=hour, minute=minute, second=second,
                              id=jobid, args=(jobid,))
        elif action == 'remove':
            """
            http://0.0.0.0:2225/scheduler/map?action=remove&jobid=z1
            """
            scheduler.remove_job(jobid)
        self.write({'res': 'success', 'job_id': jobid})


start_server([(r"/scheduler/map/?", ScheduleForRunning),
              (r"/scheduler/query", QAScheduleQuery), ], port=2225)
