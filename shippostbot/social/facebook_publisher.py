from typing import NamedTuple, Type

from ..photo import upload_photo
from ..storage.abstracts import Storage
from .abstracts import Photo, Publisher
from .facebook_api import Facebook


class FacebookPost(NamedTuple):
    id: str
    user_id: str


class FacebookComment(NamedTuple):
    id: str
    post_id: str


class FacebookPublishing(NamedTuple):
    user_id: str
    post_id: str
    comment_id: str


class FacebookPublisher(Publisher):
    def __init__(self,
                 api: Facebook,
                 storage: Type[Storage]):
        self.api = api
        self.user_api = api.get_user()

        if not storage.is_public:
            raise Exception('Provided storage must be public')
        self.storage = storage

    def publish(self, photo: Photo) -> FacebookPublishing:
        post = self.publish_photo(photo)
        comment = self.publish_comment(post.id, photo.comment)
        return FacebookPublishing(user_id=post.user_id,
                                  post_id=post.id,
                                  comment_id=comment.id)

    def publish_photo(self, photo: Photo) -> FacebookPost:
        f = upload_photo(self.storage, photo)
        res = self.user_api.publish_photo(photo.caption, f.public_url)
        f.delete()
        res.raise_for_status()
        res_json = res.json()
        return FacebookPost(id=res_json['post_id'],
                            user_id=res_json['id'])

    def publish_comment(self, post_id: str, content: str) -> FacebookComment:
        res = self.api.publish_comment(post_id, content)
        res.raise_for_status()
        res_json = res.json()
        return FacebookComment(id=res_json['id'],
                               post_id=post_id)
