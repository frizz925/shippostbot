import os
from enum import Enum
from typing import Type, Union

from ..storage import Storage, get_storage
from .abstracts import Publisher
from .facebook_publisher import (Facebook, FacebookPublisher,
                                 FacebookPublishStyle)
from .stream_publisher import StreamPublisher

__all__ = [
    'Facebook',
    'FacebookPublisher',
    'FacebookPublishStyle',
    'StreamPublisher'
]


class Publishers(Enum):
    FACEBOOK = FacebookPublisher
    STREAM = StreamPublisher


def get_publisher(publisher: Union[str, Publishers, Type[Publisher]],
                  storage: Union[str, Type[Storage]]) -> Type[Publisher]:
    if isinstance(publisher, Publisher):
        return publisher
    if isinstance(publisher, str):
        publisher = getattr(Publishers, publisher, Publishers.STREAM)

    storage = get_storage(storage)
    if publisher == Publishers.FACEBOOK:
        access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        publish_style = os.environ.get('FACEBOOK_PUBLISH_STYLE')
        if isinstance(publish_style, str):
            publish_style = getattr(FacebookPublishStyle, publish_style)
        facebook_api = Facebook(access_token, publish_style)
        return Publishers.FACEBOOK.value(facebook_api, storage)
    return publisher.value(storage)
