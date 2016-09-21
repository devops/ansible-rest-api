#!/usr/bin/env python2
# -*- coding: UTF-8 -*-


import api.v1.index
import api.v2.index
import api.v2.ansible.jobs


urls = api.v1.index.urls \
        + api.v2.index.urls \
        + api.v2.ansible.jobs.urls
