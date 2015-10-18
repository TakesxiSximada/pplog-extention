#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pit import Pit
import tornado.ioloop
import tornado.web
from zope.component import createObject
import pplog


class MainHandler(tornado.web.RequestHandler):
    def set_auth(self, username, password):
        self._username = username
        self._password = password

    def post(self):
        data = self.request.body.decode('utf8')
        pplog = createObject('pplog')
        pplog.post(data)
        self.write("OK")


class MainHandlerFactory(object):
    def __init__(self):
        conf = Pit.get('pplog', {'require': {
            'username': '',
            'password': ''}})
        self._username = conf['username']
        self._password = conf['password']

    def __call__(self, *args, **kwds):
        handler = MainHandler(*args, **kwds)
        return handler.set_auth(self._username, self._password)

application = tornado.web.Application([
    (r"/", MainHandler),
])


if __name__ == "__main__":
    pplog.includeme({})
    createObject('pplog.secret')
    application.listen(8881)
    tornado.ioloop.IOLoop.current().start()
