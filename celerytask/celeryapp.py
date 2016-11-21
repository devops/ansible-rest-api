#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

from celery import Celery
from app import config


app = Celery('celerytask',
             broker=config.CELERY_BROKER,
             backend=config.CELERY_BACKEND,
             include=["celerytask.tasks"]
             )

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_MONGODB_BACKEND_SETTINGS={
        'database': config.MONGO_NAME,
    },
)


if __name__ == "__main__":
    opts = ['-A celerytask.tasks', 'worker', '--loglevel=info']
    app.start(opts)
