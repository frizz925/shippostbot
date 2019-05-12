import logging
import sys


def create_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def init_logger():
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
