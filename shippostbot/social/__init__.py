from enum import Enum

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
