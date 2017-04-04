# Coding:utf-8


import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='quantaxis.log',
                filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


logging.info('start QUANTAXIS')

def QA_log_debug(logs):
    logging.debug(logs)
def QA_log_info(logs):
    logging.info(logs)
def QA_log_expection(logs):
    logging.exception(logs)