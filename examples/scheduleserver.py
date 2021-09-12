from QUANTAXIS.QAWebServer.schedulehandler import *
from QUANTAXIS.QAWebServer.server import start_server


def task(job_id):
    print('fin', job_id)

    
scheduler = init_scheduler()

class ScheduleForRunning(QASchedulerHandler):

    """
    添加:  get http://0.0.0.0:2225/scheduler/map?action=add&job_id=11&interval=2
    查询所有任务: gethttp://0.0.0.0:2225/scheduler?query
    """

    def get(self):
        jobid = self.get_argument('jobid', 1)
        action = self.get_argument('action', 'add')
        running_interval = self.get_argument('interval', 3)
        if action == 'add':
            scheduler.add_job(task, 'interval',
                                seconds=running_interval, id=jobid, args=(jobid,))
        elif action == 'remove':
            scheduler.remove_job(jobid)


start_server([(r"/scheduler/map/?", ScheduleForRunning),
              (r"/scheduler/query", QAScheduleQuery), ], port=2225)
