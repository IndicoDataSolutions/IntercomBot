"""
indico Test Suite
Routes - Utils
"""
import unittest, json

from intercombot.tests.mocks.request_mock import RequestHandler
from intercombot.error import InvalidJSON, MissingField, WrongFieldType
import intercombot.utils as utils

# Mock request handler
req_handler = RequestHandler()

# UnPack Tests
@utils.unpack("example", "data")
@utils.type_check(str, str)
def unpack_example(self, example, data):
    self.respond(data, code=200)

class RoutesUtilsTest(unittest.TestCase):
    def test_unpack_success(self):
        data = json.dumps({
            "example": "example text",
            "data": "example data"
        })

        unpack_example(req_handler, data)
        self.assertEqual(req_handler.data, "example data")
        self.assertEqual(req_handler.code, 200)

    def test_unpack_fail(self):
        data = json.dumps({
            "wrong": "thing"
        })
        self.assertRaises(MissingField, unpack_example, req_handler, data)

    def test_urlencoded_parse(self):
        self.assertRaises(InvalidJSON, utils.form_urlencoded_parse, "bad")
        self.assertTrue(utils.form_urlencoded_parse("data=example"), {"data": 'example'})

    def test_smart_parse(self):
        self.assertRaises(InvalidJSON, utils.smart_parse, "bad")
        self.assertTrue(utils.smart_parse("data=example"), {"data":"example"})
        self.assertTrue(utils.smart_parse("{\"data\":\"example\"}"), {"data": "example"})

    def test_wrong_type(self):
        data = json.dumps({
            "example": 1,
            "data": "example data"
        })

        self.assertRaises(WrongFieldType, unpack_example, req_handler, data)

if __name__ == "__main__":
    unittest.main()
