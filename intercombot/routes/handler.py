"""
Indico Request Handler
"""
import json, traceback

import tornado.web

from intercombot.error import IndicoError, RouteNotFound, ServerError
from intercombot.utils import LOGGER

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        return json.JSONEncoder.default(self, o)

class IndicoHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self, action):
        try:
            # Fetch appropriate handler
            if not action:
                action = "_base"

            if not hasattr(self, str(action)):
                raise RouteNotFound(action)

            # Pass along the data and get a result
            handler = getattr(self, str(action))
            result = handler(self.request.body)
            self.respond(result, 200)
        except IndicoError as e:
            self.respond(e.message, e.code)
        except Exception as e:
            LOGGER.exception("======== INDICO SERVER ERROR ========",)
            error = ServerError()
            self.respond(error.message, error.code)


    def respond(self, data, code=200):
        self.set_status(code)
        self.write(JSONEncoder().encode({
            "status": code,
            "data": data
        }))
        self.finish()
