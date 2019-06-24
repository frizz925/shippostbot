import unittest
from unittest.mock import Mock, PropertyMock

from requests import Response

from shippostbot.image import Image
from shippostbot.photo import Photo
from shippostbot.social import (Facebook, FacebookPublisher,
                                FacebookPublishStyle)
from shippostbot.storage import MemoryStorage


class MockResponse(Response):
    def __init__(self, result: dict):
        Response.__init__(self)
        self.result = result
        self.status_code = 200

    def json(self) -> dict:
        return self.result


class TestFacebookPublisher(unittest.TestCase):
    def setUp(self):
        MemoryStorage.is_public = PropertyMock(return_value=True)

        self.api = Facebook('')
        self.storage = MemoryStorage()

    def test_publish(self):
        image = Image(content=b'',
                      content_type='image/png')
        photo = Photo(name='keksimus.png',
                      caption='This is a caption',
                      comment='This is a comment',
                      image=image)

        publisher = setup_mock(FacebookPublisher(self.api, self.storage))
        res = publisher.publish(photo)
        self.assertEqual(res.user_id, 'user-id')
        self.assertEqual(res.post_id, 'post-id')
        self.assertEqual(res.comment_id, 'comment-id')

        # Test post only
        publisher = setup_mock(FacebookPublisher(self.api, self.storage, FacebookPublishStyle.POST_ONLY))
        res = publisher.publish(photo)
        self.assertEqual(res.user_id, 'user-id')
        self.assertEqual(res.post_id, 'post-id')
        self.assertIsNone(res.comment_id)


def setup_mock(publisher: FacebookPublisher) -> FacebookPublisher:
    photo_res = MockResponse({
        'id': 'user-id',
        'post_id': 'post-id'
    })
    user_api = publisher.user_api
    user_api.publish_photo = Mock(return_value=photo_res)

    comment_res = MockResponse({
        'id': 'comment-id'
    })
    api = publisher.api
    api.publish_comment = Mock(return_value=comment_res)
    return publisher


if __name__ == '__main__':
    unittest.main()
