from typing import NamedTuple, Type

from ..photo import save_photo
from ..storage import TempStorage
from ..storage.abstracts import Storage
from .abstracts import Photo, Publisher

DEFAULT_STORAGE = TempStorage()


class StreamPublishing(NamedTuple):
    caption: str
    comment: str
    image_url: str


class StreamPublisher(Publisher):
    def __init__(self, storage: Type[Storage] = DEFAULT_STORAGE):
        self.storage = storage

    def publish(self, photo: Photo) -> StreamPublishing:
        f = save_photo(self.storage, photo)
        return StreamPublishing(caption=photo.caption,
                                comment=photo.comment,
                                image_url=f.public_url)
