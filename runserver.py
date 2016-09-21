#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import os
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.process
from tornado.options import options, define
import motor

from app import config, urls


define("PORT", default=config.PORT, help="run on the given port", type=int)
define("DEBUG", default=config.DEBUG, type=bool)
define("SECRET", default=config.SECRET, type=str)
define("MONGO_HOST", default=config.MONGO_HOST, help="mongodb database host", type=str)
define("MONGO_PORT", default=config.MONGO_PORT, help="mongodb database port", type=int)
define("MONGO_NAME", default=config.MONGO_NAME, help="mongodb database name", type=str)
define("MONGO_USER", default=config.MONGO_USER, help="mongodb database user name", type=str)
define("MONGO_PASSWORD", default=config.MONGO_PASSWORD, help="mongodb database password", type=str)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = urls.urls
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "app/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "app/static"),
            cookie_secret=options.SECRET,
            xsrf_cookies=False,
            login_url="/users/login",
            debug=options.DEBUG,
        )

        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = motor.MotorClient(config.MONGO_URI)[config.MONGO_NAME]


def main():
    tornado.options.parse_command_line()
    # tornado.web.ErrorHandler = base.ErrorHandler

    if options.DEBUG:
        app_server = tornado.httpserver.HTTPServer(Application())
        print ("app App run in dev mode on %s" % options.PORT)
        app_server.listen(options.PORT)
    else:
        sockets = tornado.netutil.bind_sockets(options.PORT)
        tornado.process.fork_processes(0)
        app_server = tornado.httpserver.HTTPServer(Application())
        app_server.add_socket(sockets)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()