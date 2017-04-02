from celery import Celery
import sys
sys.path.append('c:\\quantaxis')
import QAFetch
quantaxis = Celery('tasks', backend='amqp://guest@localhost//', broker='amqp://guest@localhost//')

@quantaxis.task

def save_data(all):
  return QAFetch.QAWind()
def update_data():
  pass
def update_spider(name):
  pass
def update_all_spiders():
  pass