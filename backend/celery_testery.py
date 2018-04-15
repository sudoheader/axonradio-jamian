# not using this currently at the moment but this code 
# could be useful in the future if you want to serve this
# on a private server(so probably not that useful..)

from celery import Celery
from flask import Flask

# app = Celery('celery_testery', broker='pyamqp://guest@localhost//')
#
# @app.task
# def add(x, y):
#     return x + y

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='pyamqp://guest@localhost//',
    CELERY_RESULT_BACKEND='pyamqp://guest@localhost//'
)
celery = make_celery(flask_app)

@celery.task()
def hello_world(x, y):
    print("Hello Im a task")
