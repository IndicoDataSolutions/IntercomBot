"""
indico Test Suite
Routes > Handler
"""
import unittest

from mock import patch

from intercombot.routes.handler import IndicoHandler, JSONEncoder
from intercombot.tests.testutils.server import ServerTest
from intercombot.utils import unpack, type_check
from intercombot.error import InvalidJSON

@unpack("data")
@type_check(str)
def example(self, data):
    self.respond(data)

def bad(*args, **kwargs):
    raise InvalidJSON

@patch("intercombot.utils.smart_parse", bad)
@unpack("data")
@type_check(str)
def bad_json_example(self, data):
    pass

@unpack("data")
@type_check(str)
def raiseException(self, data):
    raise Exception()

IndicoHandler.example = example
IndicoHandler.badexample = bad_json_example
IndicoHandler.exception = raiseException


class RouteHandlerTest(ServerTest):
    routes = [(r"/(?P<action>[a-zA-Z]+)?", IndicoHandler)]
    def test_post(self):
        result = self.post("example", {
            "data": "example data"
        })

        self.assertIn("data", result)
        self.assertEqual(result["data"], "example data")


    def test_bad_post(self):
        result = self.post("example", {
            "not_data": "example data"
        })
        self.assertEqual(result["status"], 400)


    def test_exception_server(self):
        result = self.post("exception", {
            "data": "Blow Up Please"
        })

        self.assertEqual(result["status"], 500)


    def test_bad_post_missing(self):
        result = self.post("notexample", {
            "data": "example data"
        })
        self.assertEqual(result["status"], 404)


    def test_bad_json_post(self):
        result = self.post("badexample", {
            "data": "bad example"
        })
        self.assertEqual(result["status"], 400)

    def test_JSONEncoder_error(self):
        self.assertRaises(TypeError,
            JSONEncoder().encode, object())

    def test_JSONEncoder_success(self):
        data = { "sample": "sample" }
        self.assertEqual(
            JSONEncoder().encode(data),
            "{\"sample\": \"sample\"}"
        )

if __name__ == "__main__":
    unittest.main()
