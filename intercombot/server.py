import argparse

import tornado.ioloop
import tornado.web

import intercombot.config as CONFIG
from intercombot.routes.webhook import WebhookRoute
from intercombot.utils import LOGGER

def main(debug=False, port=80):
    application = tornado.web.Application([
        WebhookRoute
    ], debug = debug
     , autoreload = debug)

    LOGGER.info("Server listening on {port} in {debug} mode".format(
        port=port,
        debug="DEBUG" if debug else "PRODUCTION"
    ))

    application.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="debug mode", default=False, action="store_true")
    parser.add_argument("-p", "--port", help="hosting port", required=False, default="8000")

    args = parser.parse_args()

    main(debug=args.debug, port=args.port)
