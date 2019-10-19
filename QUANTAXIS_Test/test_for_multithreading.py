from threading import Thread
def test():
    import QUANTAXIS as QA
    global QA
    QA.QA_util_log_info('指数日线')

if __name__ == '__main__':
    t = Thread(target=test, args=())
    t.start()
    t.join()
    import QUANTAXIS as QA
    QA.QA_util_log_info('指数日线')