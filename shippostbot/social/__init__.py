import os
from enum import Enum
from typing import Type, Union

from ..storage import Storage, get_storage
from .abstracts import Publisher
from .facebook_publisher import Facebook, FacebookPublisher
from .stream_publisher import StreamPublisher

__all__ = [
    'Facebook',
    'FacebookPublisher',
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
        facebook_api = Facebook(access_token)
        return Publishers.FACEBOOK.value(facebook_api, storage)
    return publisher.value(storage)
