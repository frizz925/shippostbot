import unittest

import requests

from shippostbot.social.facebook_api import Facebook


class TestFacebookAPI(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.api = Facebook('mock-token', session=self.session)


if __name__ == '__main__':
    unittest.main()
