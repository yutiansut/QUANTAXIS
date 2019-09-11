import subprocess
# named pipe Server
# encoding: utf-8

import os
import subprocess
import time

import logging


read_path = "/tmp/server_in.pipe"
#write_path = "/tmp/server_out.pipe"



if __name__ == '__main__':

    logging.basicConfig(filename='parent_process.log', level=logging.DEBUG)

    try:
        # 创建命名管道
        #os.mkfifo(write_path)
        os.mkfifo(read_path)
    except OSError as e:
        # 如果命名管道已经创建过了，那么无所谓
        print("mkfifo error:", e)

    p = subprocess.Popen(['python', './QUANTAXIS_Test/QAUtil_Test/QA_TestSubProcess.py'],
                         cwd='/Users/jerryw/MyCode/QUANTAXIS',
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 写入和读取的文件，正好和Client相反
    rf = os.open(read_path, os.O_RDONLY)
    #f = os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)

    while True:
        # 接收请求
        s = os.read(rf, 2)
        if len(s) == 0:
            # 没有收到字符，一般是唯一的发送方被关闭了。
            # 这里可以休息一下继续，对后续消息没有任何影响，也不会丢包。
            time.sleep(1)
            continue

        # 如果收到的字符串带一个s，打印出来
        # 用于调试和测试
        if b"z" in s:
            print("received", s)

        # 在请求前面加一个s字母，返回
        #os.write(f, s)
        print(s)



    sz = len('ok, task is running 1')

    #p.stdin.write(b"002417")

    while( True ):
        s = p.stdout.read(sz)
        print(s)
        if len(s) == 0:
            break;


    p.wait()

    pass