#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import json
from bson import json_util
from tornado import gen
from base import APIHandler


class IndexHandler(APIHandler):

    @gen.coroutine
    def get(self, *args, **kwargs):
        """ """

        doc = {"msg": "App rest api server"}
        self.write(json.dumps(doc, default=json_util.default))

urls = [
    (r"/api/v1", IndexHandler),
]
