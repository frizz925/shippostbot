import logging
import os
from typing import Type, Union

from . import image, log
from .photo import create_photo
from .post import SelectionType, create_post, get_selection_type
from .social import get_publisher
from .social.abstracts import Publisher
from .storage.abstracts import Storage


def main_from_env() -> dict:
    return main(os.environ.get('SELECTION_TYPE', ''),
                os.environ.get('SOCIAL_PUBLISHER', ''),
                os.environ.get('STORAGE_TYPE', ''))


def main(selection_type: Union[str, SelectionType],
         publisher: Union[str, Type[Publisher]],
         storage: Union[str, Type[Storage]]) -> dict:
    log.init_logger()
    selection_type = get_selection_type(selection_type)
    publisher = get_publisher(publisher, storage)

    post = create_post(selection_type)
    if post is None:
        raise Exception('Unable to create post!')
    photo = create_photo(post)
    return publisher.publish(photo)._asdict()


def setup_from_env():
    set_logging_level(os.environ.get('LOGGING_LEVEL', ''))


def set_logging_level(logging_level: str):
    logging_level = getattr(logging, logging_level, log.LOGGING_LEVEL)
    log.LOGGING_LEVEL = logging_level


def set_cloudwatch(enabled: bool):
    log.CLOUDWATCH_ENABLED = enabled


__all__ = ['image', 'log']
