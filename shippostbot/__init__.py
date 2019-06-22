import logging
import os
from typing import Type, Union

from . import image, log
from .photo import create_photo
from .post import SelectionType, create_post
from .social import Facebook, Publishers
from .social.abstracts import Publisher
from .storage import S3Bucket, Storages
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


def get_selection_type(selection_type: Union[str, SelectionType]) -> SelectionType:
    if isinstance(selection_type, SelectionType):
        return selection_type
    return getattr(SelectionType, selection_type, SelectionType.FROM_CHARACTER_TO_MEDIA)


def get_publisher(publisher: Union[str, Type[Publisher]],
                  storage: Union[str, Type[Storage]]) -> Type[Publisher]:
    if isinstance(publisher, Publisher):
        return publisher

    storage = get_storage(storage)
    publisher = getattr(Publishers, publisher, Publishers.STREAM)
    if publisher == Publishers.FACEBOOK:
        access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        facebook_api = Facebook(access_token)
        return Publishers.FACEBOOK.value(facebook_api, storage)
    return publisher.value(storage)


def get_storage(storage: Union[str, Type[Storage]]) -> Type[Storage]:
    if isinstance(storage, Storage):
        return storage
    storage = getattr(Storages, storage, Storages.TEMP_FILE)
    if storage == Storages.AWS_S3:
        region = os.environ.get('S3_REGION')
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        bucket = S3Bucket(region, bucket_name, 'public-read')
        return Storages.AWS_S3.value(bucket)
    return storage.value()


def setup_from_env():
    set_logging_level(os.environ.get('LOGGING_LEVEL', ''))


def set_logging_level(logging_level: str):
    logging_level = getattr(logging, logging_level, log.LOGGING_LEVEL)
    log.LOGGING_LEVEL = logging_level


def set_cloudwatch(enabled: bool):
    log.CLOUDWATCH_ENABLED = enabled


__all__ = ['image', 'log']
