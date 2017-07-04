import datetime
from subprocess import *


webs = ['www.baidu.com']


def QA_web_ping(url):
    ms_list = []

    p = Popen(["ping", url],
              stdin=PIPE, stdout=PIPE, stderr=PIPE,
              shell=True)
    out = p.stdout.read()
    list = str(out).split('=')
    for item in list:
        if 'ms' in item:
            ms_list.append(int(item.split('ms')[0]))
    return ms_list[-1]


import os


if __name__ == "__main__":
    print(datetime.datetime.now())
    print(QA_web_ping('www.baidu.com'))
    print(datetime.datetime.now())