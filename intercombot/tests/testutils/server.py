"""
indico Test Utils for Running Servers
"""
import json, logging

from tornado.web import Application
from tornado.testing import AsyncHTTPTestCase

# Disable tornado access warnings
logging.getLogger("tornado.access").propagate = False
logging.getLogger("tornado.access").addHandler(logging.NullHandler())

class ServerTest(AsyncHTTPTestCase):
    def setUp(self):
        super(ServerTest, self).setUp()
        name = str(self).split(" ")
        self.name = name[0].replace("_","") + name[1].split(".")[-1][:-1]

    def get_app(self):
        return Application(self.routes, debug = False)

    def post(self, route, data):
        result = self.fetch("/%s" % route, method = "POST",
                                body = json.dumps(data)).body

        try:
            return json.loads(result)
        except ValueError:
            raise ValueError(result)


    def tearDown(self):
        super(ServerTest, self).tearDown()
