# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import hashlib
import time

from QUANTAXIS.QASetting.cache import get_cache


# Globals ######################################################################
DEBUG = False


class CronTabItem(_CronTab):
    """A cron tab schedule.
    :param str cronschedule: The cron schedule.  E.g. ``@daily``,
        ``0   0    *    *     */2     *``.  `See the project page for more
        information <https://github.com/josiahcarlson/parse-crontab>`_.
    """
    def __init__(self, cronschedule):
        self.__schedule = cronschedule
        super(CronTabItem, self).__init__(cronschedule)

    @property
    def schedule(self):
        return self.__schedule

    def next_time(self, asc=False):
        """Get the local time of the next schedule time this job will run.
        :param bool asc: Format the result with ``time.asctime()``
        :returns: The epoch time or string representation of the epoch time that
            the job should be run next
        """
        _time = time.localtime(time.time() + self.next())

        if asc:
            return time.asctime(_time)

        return time.mktime(_time)


class CronTab(object):
    """Represents a set of cron jobs, much like a crontab file.  The jobs will
    be given an ID (md5 hash of description + command + schedule).  If the job
    already exists in the cache, "last-run" and "last-run-result" will be read
    from the cache.  If the job does not exist in the cache, it will be added.
    :param list jobs: A list of dictionaries representing a job
    """
    def __init__(self, jobs):
        cache = get_cache()
        self.jobs = []

        for job in jobs:
            m = hashlib.md5()
            m.update(job["description"])
            m.update(job["command"])
            m.update(job["cron-job"])
            job["id"] = m.hexdigest()
            job["cron-job"] = CronTabItem(job["cron-job"])
            job["next-run"] = job["cron-job"].next_time()

            cached = cache.get(job["id"])
            if cached:
                job["last-run"] = cached["last-run"]
                job["last-run-result"] = cached["last-run-result"]
            else:
                job["last-run"] = 0
                job["last-run-result"] = 0
                cache.add_job(job)

            self.jobs.append(job)