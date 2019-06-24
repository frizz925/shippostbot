from enum import Enum
from typing import NamedTuple, Optional, Type

from ..log import create_logger
from ..photo import upload_photo
from ..storage.abstracts import Storage
from .abstracts import Photo, Publisher
from .facebook_api import Facebook


class FacebookPublishStyle(Enum):
    POST_ONLY = 0
    POST_AND_COMMENT = 1


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
                 storage: Type[Storage],
                 publish_style: Optional[FacebookPublishStyle] = None):
        self.api = api
        self.user_api = api.get_user()
        self.logger = create_logger(FacebookPublisher)

        if publish_style is None:
            self.publish_style = FacebookPublishStyle.POST_AND_COMMENT
        else:
            self.publish_style = publish_style

        if not storage.is_public:
            raise Exception('Provided storage must be public')
        self.storage = storage

    def publish(self, photo: Photo) -> FacebookPublishing:
        if self.publish_style == FacebookPublishStyle.POST_ONLY:
            caption = '%s\r\n\r\n%s' % (photo.caption, photo.comment)
            post = self.publish_photo(photo, caption)
            return FacebookPublishing(user_id=post.user_id,
                                      post_id=post.id,
                                      comment_id=None)
        else:
            post = self.publish_photo(photo)
            comment = self.publish_comment(post.id, photo.comment)
            return FacebookPublishing(user_id=post.user_id,
                                      post_id=post.id,
                                      comment_id=comment.id)

    def publish_photo(self,
                      photo: Photo,
                      caption: Optional[str] = None) -> FacebookPost:
        if caption is None:
            caption = photo.caption
        f = upload_photo(self.storage, photo)
        self.logger.info(
            'publish_photo() start, caption: "%s", image_url: "%s", content_type: "%s"' %
            (caption, f.public_url, photo.image.content_type)
        )
        res = self.user_api.publish_photo(caption, f.public_url)
        f.delete()
        res_json = res.json()
        self.logger.info('publish_photo() result: %s' % res_json)
        res.raise_for_status()
        return FacebookPost(id=res_json['post_id'],
                            user_id=res_json['id'])

    def publish_comment(self, post_id: str, content: str) -> FacebookComment:
        self.logger.info(
            'publish_comment() start, post_id: "%s", content: "%s"' %
            (post_id, content)
        )
        res = self.api.publish_comment(post_id, content)
        res_json = res.json()
        self.logger.info('publish_comment() result: %s' % res_json)
        res.raise_for_status()
        return FacebookComment(id=res_json['id'],
                               post_id=post_id)
