#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import json
from bson import json_util
from schema import Schema, SchemaError, Optional
from celerytask import tasks

from app.api.v1.base import APIHandler, authenticated


class AdhocJobsHandler(APIHandler):


    def post(self):
        adhoc_schema = Schema({
            'host_list': basestring,
            'module_name': basestring,
            'module_args': basestring,
            'pattern': basestring,
            Optional('forks'): int,
            Optional('play_name'): basestring,

        })
        try:
            job_data = adhoc_schema.validate(json.loads(self.request.body))
        except SchemaError as e:
            self.write(json.dumps({"error": e.message}))
        else:
            job = tasks.ansible_adhoc.delay(
                host_list=job_data['host_list'],
                module_name=job_data['module_name'],
                module_args=job_data['module_args'],
                pattern=job_data['pattern']
            )
            self.write(json.dumps({"task_id": job.id}, default=json_util.default))
            self.set_status(202)
            self.set_header("Location", "/api/v2/ansible/jobs/status/" + job.id)


class PlaybookJobsHandler(APIHandler):

    def post(self, *args, **kwargs):
        playbook_schema = Schema({
            'playbook': basestring,
            'host_list': basestring,
            'module_path': basestring
        })
        try:
            job_data = playbook_schema.validate(json.loads(self.request.body))
        except SchemaError as e:
            self.write(json.dumps({"error": e.message}))
        else:
            job = tasks.ansible_playbook.delay(
                playbook=job_data['playbook'],
                host_list=job_data['host_list'],
                module_path=job_data['module_path']
            )
            self.write(json.dumps({"task_id": job.id}, default=json_util.default))
            self.set_status(202)
            self.set_header("Location", "/api/v2/ansible/jobs/status/" + job.id)

class AnsibleJobStatusHandler(APIHandler):
    def get(self, task_id):
        task = tasks.ansible_adhoc.AsyncResult(task_id)
        response = {
            'task_id': task_id,
            'state': task.state,
            'result': task.info
        }
        self.write(json.dumps(response))

urls = [
    (r"/api/v2/ansible/jobs/adhocs", AdhocJobsHandler),
    (r"/api/v2/ansible/jobs/playbooks", PlaybookJobsHandler),
    (r"/api/v2/ansible/jobs/status/(.*)", AnsibleJobStatusHandler),

]
