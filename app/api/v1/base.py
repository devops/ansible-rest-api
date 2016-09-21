#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import tornado.web
import tornado.escape
import json
import functools


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.get_api_key():
            self.redirect("/users/login")
        return method(self, *args, **kwargs)
    return wrapper


class APIHandler(tornado.web.RequestHandler):
    """ """

    @property
    def db(self):
        return self.application.db

    def prepare(self):
        # if auth:
        #     self.is_authenticated()
        pass

    def get_current_user(self):
        user_json = self.get_secure_cookie("username")
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def write_error(self, status_code, **kwargs):
        if self._status_code == 404:
            self.write(json.dumps({"error": "page not found"}))
        elif self._status_code == 500:
            self.write(json.dumps({"error": "500"}))
        else:
            self.write(json.dumps({"error": self._status_code}))

    def get_api_key(self):
        return self.get_argument("apikey", False)
        # if self.get_argument("code", False):
        #     user = self.db.users.find_one({"code": self.get_argument("code")})
        # return self.get_argument("apikey")


class APIError(tornado.web.HTTPError):
    """需要向前端输出错误异常时，请直接在 Handler 中使用 raise APIError() 即可"""
    def __init__(self, status_code, *args, **kwargs):
        super(APIError, self).__init__(status_code, *args, **kwargs)
