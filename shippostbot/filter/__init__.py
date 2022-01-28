from enum import Enum

from .abstracts import PostFilter
from .file_filter import file_filter

__all__ = [
    'PostFilter',
    'file_filter',
]


class Filters(Enum):
    FILE = file_filter
