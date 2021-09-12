from QUANTAXIS.QAWebServer.schedulehandler import *
from QUANTAXIS.QAWebServer.server import start_server


def task(job_id):
    print('fin', job_id)

    
scheduler = init_scheduler()

class ScheduleForRunning(QASchedulerHandler):

    """
    http://0.0.0.0:2225/scheduler?job_id=1&action=add

    """

    def get(self):
        jobid = self.get_argument('jobid', 1)

        running_interval = self.get_argument('interval', 3)

        scheduler.add_job(task, 'interval',
                            seconds=running_interval, id=jobid, args=(jobid,))



start_server([(r"/scheduler/map/?", ScheduleForRunning),
              (r"/scheduler/query", QAScheduleQuery), ], port=2225)
