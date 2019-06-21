from abc import ABC, abstractmethod
from typing import NamedTuple, Type

from ..photo import Photo


class Publisher(ABC):
    @abstractmethod
    def publish(self, photo: Photo) -> Type[NamedTuple]:
        return None
