from celery import Celery

quantaxis = Celery('tasks', backend='amqp://guest@localhost//', broker='amqp://guest@localhost//')

@quantaxis.task

def save_data():
  pass
def update_data():
  pass
def update_spider(name):
  pass
def update_all_spiders():
  pass