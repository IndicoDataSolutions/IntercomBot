"""
Indico Request/Response Utils
"""
import os, sys, json, urlparse, logging

from intercombot.error import MissingField, InvalidJSON
from intercombot.error import WrongFieldType

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
# Turn down requests log verbosity
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOGGER = logging.getLogger("indico")
LOGGER.setLevel(logging.DEBUG)

# All Output
fileHandler = logging.FileHandler(os.path.join(LOG_PATH, "intercombot_output.log"))
fileHandler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
fileHandler.setLevel(logging.DEBUG)
LOGGER.addHandler(fileHandler)

# Error logging
fileHandler = logging.FileHandler(os.path.join(LOG_PATH, "intercombot_error.log"))
fileHandler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
fileHandler.setLevel(logging.WARNING)
LOGGER.addHandler(fileHandler)

# Standard Output
stdout = logging.StreamHandler(sys.stdout)
stdout.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
stdout.setLevel(logging.DEBUG)
LOGGER.addHandler(stdout)

def unpack(*arguments):
    """
    Unpack arguments to be used in methods wrapped
    """
    def decorator(func):
        def wrapper(_self, data, **kwargs):
            data = smart_parse(data)
            try:
                args = [data[item] for item in arguments]
            except KeyError:
                raise MissingField(item)

            kwargs["_arguments"] = arguments

            func(_self, *args, **kwargs)
        return wrapper
    return decorator

def type_check(*types):
    """
    Checks unpacked arguments for types
    """
    def decorator(func):
        def wrapper(_self, *args, **kwargs):
            for arg, _type, _arg in zip(args, types, kwargs.pop("_arguments")):
                if not isinstance(arg, _type):
                    if _type is str and isinstance(arg, unicode):
                        continue
                    raise WrongFieldType(_arg, arg, _type)
            func(_self, *args, **kwargs)
        return wrapper
    return decorator


def form_urlencoded_parse(body):
    """
    Parse x-www-form-url encoded data
    """
    try:
        data = urlparse.parse_qs(body, strict_parsing=True)
        for key in data:
            data[key] = data[key][0]
        return data
    except ValueError:
        raise InvalidJSON()

def smart_parse(body):
    """
    Handle json, fall back to x-www-form-urlencoded
    """
    try:
        data_dict = json.loads(body)
    except ValueError:
        return form_urlencoded_parse(body)
    return data_dict
