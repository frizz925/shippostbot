from typing import Dict

from .abstracts import File, Storage


class MemoryStorage(Storage):
    mapping: Dict[str, bytes]

    def __init__(self):
        self.mapping = {}

    def read(self, name: str) -> bytes:
        return self.mapping.get(name)

    def save(self,
             name: str,
             content: bytes,
             content_type: str = 'application/octet-stream') -> File:
        self.mapping[name] = content
        return File(self, name, content_type)

    def delete(self, name: str):
        if name in self.mapping:
            del self.mapping[name]
