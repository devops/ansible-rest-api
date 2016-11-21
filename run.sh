#!/bin/bash

export PYTHONOPTIMIZE=1
export ANSIBLE_HOST_KEY_CHECKING=0

nohup celery worker --app=celerytask.celeryapp.app -l info &
nohup python runserver.py &
