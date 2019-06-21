from __future__ import annotations

import os
import tempfile

from .abstracts import File, Storage


class TempFile(File):
    storage: TempStorage

    def __init__(self,
                 storage: TempStorage,
                 path: str):
        File.__init__(self, storage, path, None)

    @property
    def content(self) -> bytes:
        return self.storage.read(self.path)

    @property
    def path(self) -> str:
        return self.name

    @property
    def public_url(self) -> str:
        return 'file://' + self.path


class TempStorage(Storage):
    def __init__(self):
        self.tmp_dir = tempfile.gettempdir()

    def read(self, path: str) -> bytes:
        with open(path, 'rb') as f:
            return f.read()

    def save(self,
             name: str,
             content: bytes,
             content_type=None) -> TempFile:
        path = os.path.join(self.tmp_dir, name)
        with open(path, 'wb') as f:
            f.write(content)
        return TempFile(self, path)

    def delete(self, path: str):
        os.remove(path)
