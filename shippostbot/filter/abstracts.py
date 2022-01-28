from abc import ABC, abstractmethod
from typing import Callable
from ..entities import Post

PostFilter = Callable[[Post], bool]
