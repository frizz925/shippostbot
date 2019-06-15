import inspect
import logging
import os
import sys

CLOUDWATCH_ENABLED = False
STDOUT_LEVEL = logging.INFO
STDERR_LEVEL = logging.WARN

def create_logger(obj) -> logging.Logger:
    if inspect.isclass(obj) or inspect.isfunction(obj):
        name = obj.__name__
    elif isinstance(obj, object):
        name = obj.__class__.__name__
    else:
        name = obj
    return logging.getLogger(name)


def init_logger():
    if CLOUDWATCH_ENABLED:
        fmt = '[%(name)s] [%(levelname)s] %(message)s'
        formatter = logging.Formatter(fmt)
    else:
        fmt = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
        formatter = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')

    stdout = logging.StreamHandler(stream=sys.stdout)
    stdout.setFormatter(formatter)
    stdout.setLevel(STDOUT_LEVEL)
    stderr = logging.StreamHandler(stream=sys.stderr)
    stderr.setFormatter(formatter)
    stderr.setLevel(STDERR_LEVEL)

    logger = logging.getLogger()
    logger.setLevel(STDOUT_LEVEL)
    logger.handlers = [stdout, stderr]
