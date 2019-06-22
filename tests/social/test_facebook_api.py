import unittest
from unittest.mock import MagicMock

from requests import Response, Session

from shippostbot.social.facebook_api import Facebook


class TestFacebookAPI(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        self.api = Facebook('', session=self.session)
        self.user_api = self.api.get_user()

    def test_publish_comment(self):
        mock_response = Response()
        self.mock_response(mock_response)
        res = self.api.publish_comment('123456_3456789', 'This is a mock message')
        self.assertEqual(res, mock_response)

    def test_publish_photo(self):
        mock_response = Response()
        self.mock_response(mock_response)
        res = self.user_api.publish_photo('This is a nice photo', 'file:///dev/null')
        self.assertEqual(res, mock_response)

    def mock_response(self, res: Response):
        session = self.session
        session.send = MagicMock()
        session.send.return_value = res


if __name__ == '__main__':
    unittest.main()
