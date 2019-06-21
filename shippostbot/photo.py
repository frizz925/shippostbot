from hashlib import sha1
from typing import NamedTuple, Type

from .entities import Post
from .image import Image, combine_images
from .storage.abstracts import File, Storage


class Photo(NamedTuple):
    name: str
    image: Image
    caption: str
    comment: str


def create_photo(post: Post) -> Photo:
    images = [c.image_url for c in post.characters]
    image = combine_images(*images)
    m = sha1()
    m.update(image.content)
    return Photo(name='%s.png' % m.hexdigest(),
                 image=image,
                 caption=post.caption,
                 comment=post.comment)


def save_photo(storage: Type[Storage], photo: Photo) -> Type[File]:
    image = photo.image
    return storage.save(photo.name, image.content, image.content_type)


def upload_photo(storage: Type[Storage], photo: Photo) -> Type[File]:
    if not storage.is_public:
        raise Exception('Provided storage must be public')
    return save_photo(storage, photo)
