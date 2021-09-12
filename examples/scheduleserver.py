from QUANTAXIS.QAWebServer.schedulehandler import QASchedulerHandler
from QUANTAXIS.QAWebServer.server import start_server


def task():
    print('fin')


class ScheduleForRunning(QASchedulerHandler):

    """
    http://0.0.0.0:2225/scheduler?job_id=1&action=add

    """

    def get(self):
        jobid = self.get_argument('jobid')
        scheduler.add_job(task, 'interval',
                          seconds=3, id=jobid, args=(jobid,))


start_server([(r"/scheduler/map/?", QASchedulerHandler), ], port=2225)
