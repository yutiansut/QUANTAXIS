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


import sqlite3
import os

CACHE = None


def _init(cache_file):
    """Creates a new Cache object."""
    global CACHE
    CACHE = Cache(cache_file)


def get_cache(config_file=None):
    """Used to retrieve the global cache object."""
    if CACHE is None:
        _init(config_file)

    return CACHE


class Cache():
    """This object is used to interface with the job cache.  It uses a SQLite3
    database to store the information.
    :param str cache_file: The path to the cache file.  This will be created if
        it does not already exist.
    """
    def __init__(self, cache_file):
        self.filename = cache_file

        if not os.path.isfile(self.filename):
            self._create(self.filename)

        self.conn = sqlite3.connect(self.filename)
        self.cur = self.conn.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON")

    def __del__(self):
        """Commit the changes and close the connection."""
        if getattr(self, "conn", None):
            self.conn.commit()
            self.conn.close()

    def _create(self, cache_file):
        """Create the tables needed to store the information."""
        conn = sqlite3.connect(cache_file)
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute('''
            CREATE TABLE jobs(
                hash TEXT NOT NULL UNIQUE PRIMARY KEY, description TEXT NOT NULL,
                last_run REAL, next_run REAL, last_run_result INTEGER)''')

        cur.execute('''
            CREATE TABLE history(
                hash TEXT, description TEXT, time REAL, result INTEGER,
                FOREIGN KEY(hash) REFERENCES jobs(hash))''')

        conn.commit()
        conn.close()

    def has(self, job):
        """Checks to see whether or not a job exists in the table.
        :param dict job: The job dictionary
        :returns: True if the job exists, False otherwise
        """
        return bool(self.cur.execute('SELECT count(*) FROM jobs WHERE hash=?', (job["id"],)))

    def get(self, id):
        """Retrieves the job with the selected ID.
        :param str id: The ID of the job
        :returns: The dictionary of the job if found, None otherwise
        """
        self.cur.execute("SELECT * FROM jobs WHERE hash=?", (id,))
        item = self.cur.fetchone()
        if item:
            return dict(zip(
                ("id", "description", "last-run", "next-run", "last-run-result"),
                item))

        return None

    def update(self, job):
        """Update last_run, next_run, and last_run_result for an existing job.
        :param dict job: The job dictionary
        :returns: True
        """
        self.cur.execute('''UPDATE jobs
            SET last_run=?,next_run=?,last_run_result=? WHERE hash=?''', (
            job["last-run"], job["next-run"], job["last-run-result"], job["id"]))

    def add_job(self, job):
        """Adds a new job into the cache.
        :param dict job: The job dictionary
        :returns: True
        """
        self.cur.execute("INSERT INTO jobs VALUES(?,?,?,?,?)", (
            job["id"], job["description"], job["last-run"], job["next-run"], job["last-run-result"]))

        return True

    def add_result(self, job):
        """Adds a job run result to the history table.
        :param dict job: The job dictionary
        :returns: True
        """
        self.cur.execute(
            "INSERT INTO history VALUES(?,?,?,?)",
            (job["id"], job["description"], job["last-run"], job["last-run-result"]))

        return True