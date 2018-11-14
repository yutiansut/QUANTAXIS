# named pipe Client
# encoding: utf-8

import os
import sys
import time

import logging


write_path = '/tmp/server_in.pipe'
#read_path = '/tmp/server_out.pipe'


if __name__ == '__main__':

    logging.basicConfig(filename='sub_process.log', level=logging.DEBUG)


    counter = 1

    logging.debug('call os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR) >')

    f = os.open(write_path, os.O_RDWR)
    print("Client open f", f)

    logging.debug('finish call the os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR)')

    rf = None

    while True:

        logging.debug("ready Client发送请求")
        # Client发送请求
        req = ("%s ")%counter

        logging.debug("ready  os.write(f, req)")
        len_send = os.write(f, req)
        logging.debug("finish ready  os.write(f, req)")


        print("request", req, len_send)
        logging.debug("request", req, len_send)

        counter += 1

        if rf == None:
            # *要点1：在这里第一次打开read_path，实际这里的open是一个阻塞操作
            # 打开的时机很重要。如果在程序刚开始，没发送请求就打开read_path，肯定会阻塞住
            logging.debug("ready rf = os.open(read_path, os.O_RDONLY)", rf)
            #rf = os.open(read_path, os.O_RDONLY)
            print("client opened rf", rf)

            logging.debug("finish client opened rf", rf)

            # 接收Server回应
        #s = os.read(rf, 1024)
        #if len(s) == 0:
            # 一般来说，是管道被意外关闭了，比如Server退出了
        #    break

        #print("received", s)

    os.close(f)
    #os.close(rf)

    for i in range(10):
        time.sleep(1)
        print("ok, task is running %d %s"%i, n)

    pass