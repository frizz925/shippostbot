import logging
import sys


def init_logger():
    fmt = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
    formatter = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')

    stdout = logging.StreamHandler(stream=sys.stdout)
    stdout.setFormatter(formatter)
    stdout.setLevel(logging.INFO)
    stderr = logging.StreamHandler(stream=sys.stderr)
    stderr.setFormatter(formatter)
    stderr.setLevel(logging.WARN)

    logger = get_logger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(stdout)
    logger.addHandler(stderr)


def get_logger() -> logging.Logger:
    return logging.getLogger()


def info(msg, *args, **kwargs):
    get_logger().info(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    get_logger().info(msg, *args, **kwargs)
