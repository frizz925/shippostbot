from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type


class File(object):
    def __init__(self,
                 storage: Type[Storage],
                 name: str,
                 content_type: str):
        self.storage = storage
        self.name = name
        self.content_type = content_type

    @property
    def content(self) -> bytes:
        return self.storage.read(self.name)

    @property
    def path(self) -> str:
        return None

    @property
    def public_url(self) -> str:
        return None

    def save(self, content: bytes, content_type=None) -> Type[File]:
        if content_type is None:
            content_type = self.content_type
        return self.storage.save(self.name, content, content_type)

    def save_to_storage(self, storage: Type[Storage]) -> Type[File]:
        return storage.save_file(self)

    def delete(self):
        self.storage.delete(self.name)

    def delete_from_storage(self, storage: Type[Storage]):
        storage.delete_file(self)


class Storage(ABC):
    @property
    def is_public(self):
        return False

    @abstractmethod
    def read(self, name: str) -> bytes:
        return None

    @abstractmethod
    def save(self,
             name: str,
             content: bytes,
             content_type='application/octet-stream') -> Type[File]:
        return File(self, name, content_type)

    def save_file(self, f: Type[File]) -> Type[File]:
        return self.save(f.name, f.content, f.content_type)

    @abstractmethod
    def delete(self, name: str):
        pass

    def delete_file(self, f: Type[File]):
        return self.delete(f.name)
