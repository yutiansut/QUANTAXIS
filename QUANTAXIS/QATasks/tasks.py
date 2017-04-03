from celery import Celery
import QUANTAXIS

quantaxis = Celery('tasks', backend='amqp://guest@localhost//', broker='amqp://guest@localhost//')

@quantaxis.task

def save_data(all):
  pass
def update_data():
  pass
def update_spider(name):
  pass
def update_all_spiders():
  pass