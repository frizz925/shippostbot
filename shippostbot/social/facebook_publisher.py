from typing import NamedTuple, Type

from ..log import create_logger
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
        self.logger = create_logger(FacebookPublisher)

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
        self.logger.info('publish_photo() start, ' +
                         'caption: "' + photo.caption +
                         '", image_url: "' + f.public_url +
                         '", content_type: "' + photo.image.content_type + '"')
        res = self.user_api.publish_photo(photo.caption, f.public_url)
        f.delete()
        res_json = res.json()
        self.logger.info('publish_photo() result: ' + res_json)
        res.raise_for_status()
        return FacebookPost(id=res_json['post_id'],
                            user_id=res_json['id'])

    def publish_comment(self, post_id: str, content: str) -> FacebookComment:
        self.logger.info('publish_comment() start, ' +
                         'post_id: "' + post_id +
                         '", content: "' + content + '"')
        res = self.api.publish_comment(post_id, content)
        res_json = res.json()
        self.logger.info('publish_comment() result: ' + res_json)
        res.raise_for_status()
        return FacebookComment(id=res_json['id'],
                               post_id=post_id)
