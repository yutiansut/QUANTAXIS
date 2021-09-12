from datetime import datetime
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import RequestHandler, Application
from apscheduler.schedulers.tornado import TornadoScheduler
import threading
from QAWebServer.basehandles import QABaseHandler
from qaenv import mongo_ip, mongo_port
from apscheduler.jobstores.mongodb import MongoDBJobStore
import pymongo
"""
增加 mongodb 的数据读取

"""
scheduler = None
job_ids = []
jobstores = {
    'default': MongoDBJobStore(database='qascheduler', collection='jobs', client=pymongo.MongoClient(host=mongo_ip, port=mongo_port))
}
# 初始化


def init_scheduler():
    global scheduler
    scheduler = TornadoScheduler(jobstores=jobstores)
    scheduler.start()
    print('[QAScheduler Init]APScheduler has been started')

# 要执行的定时任务在这里


def task1(options):
    print('{} [QASchedule][Task]-{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), options))
    # print(threading.enumerate())


class QASchedulerHandler(QABaseHandler):
    """
    http://0.0.0.0:8010/scheduler?job_id=1&action=add
    """

    def get(self):
        global job_ids
        job_id = self.get_query_argument('job_id', None)
        action = self.get_query_argument('action', None)
        if job_id:
            # add
            if 'add' == action:
                if job_id not in job_ids:
                    job_ids.append(job_id)
                    scheduler.add_job(task1, 'interval',
                                      seconds=3, id=job_id, args=(job_id,))
                    self.write('[TASK ADDED] - {}'.format(job_id))
                else:
                    self.write('[TASK EXISTS] - {}'.format(job_id))
            # remove
            elif 'remove' == action:
                if job_id in job_ids:
                    scheduler.remove_job(job_id)
                    job_ids.remove(job_id)
                    self.write('[TASK REMOVED] - {}'.format(job_id))
                else:
                    self.write('[TASK NOT FOUND] - {}'.format(job_id))
        else:
            self.write('[INVALID PARAMS] INVALID job_id or action')


def format_joboutput(job):
    return {
        'id': job.id,
        'name': job.name,
        'args': job.args,
        'kwards': job.kwargs,
        'coalesce': job.coalesce,
        'nextruntime': str(job.next_run_time)
    }


class QAScheduleQuery(QABaseHandler):
    def get(self):
        action = self.get_argument('action', None)
        print(action)
        if action == 'queryall':
            jobs = scheduler.get_jobs()
            print([format_joboutput(x) for x in jobs])
            self.write({'res': [format_joboutput(x) for x in jobs]})
