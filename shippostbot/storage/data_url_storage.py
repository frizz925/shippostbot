from __future__ import annotations

from base64 import b64encode
from typing import Optional

from .abstracts import File, Storage


class DataUrlFile(File):
    def __init__(self,
                 content: bytes,
                 content_type: str):
        File.__init__(self, None, None, content_type)
        self._content = content

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def public_url(self) -> str:
        content_b64 = b64encode(self.content).decode('utf-8')
        return 'data:%s;base64,%s' % (self.content_type, content_b64)

    def save(self,
             content: bytes,
             content_type: Optional[str] = None) -> DataUrlFile:
        if content_type is None:
            content_type = self.content_type
        return DataUrlFile(content, content_type)

    def delete(self):
        pass


class DataUrlStorage(Storage):
    @property
    def is_public(self):
        return True

    def read(self, name: str) -> bytes:
        raise NotImplementedError('Data URL storage doesn\'t support read method')

    def save(self,
             name: str,
             content: bytes,
             content_type: str = 'application/octet-stream') -> DataUrlFile:
        return DataUrlFile(content, content_type)

    def delete(self, name: str):
        pass
