import inspect
import logging
import os
import sys


def create_logger(obj) -> logging.Logger:
    if inspect.isclass(obj) or inspect.isfunction(obj):
        name = obj.__name__
    elif isinstance(obj, object):
        name = obj.__class__.__name__
    else:
        name = obj
    return logging.getLogger(name)


def init_logger():
    cloudwatch_enabled = os.environ.get('CLOUDWATCH_ENABLED', False) is not False
    if cloudwatch_enabled:
        fmt = '[%(name)s] [%(levelname)s] %(message)s'
        formatter = logging.Formatter(fmt)
    else:
        fmt = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
        formatter = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')

    stdout = logging.StreamHandler(stream=sys.stdout)
    stdout.setFormatter(formatter)
    stdout.setLevel(logging.INFO)
    stderr = logging.StreamHandler(stream=sys.stderr)
    stderr.setFormatter(formatter)
    stderr.setLevel(logging.WARN)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers = [stdout, stderr]
