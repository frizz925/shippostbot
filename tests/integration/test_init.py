import logging
import os
import unittest

import shippostbot
from shippostbot.post import SelectionType


class TestMain(unittest.TestCase):
    def test_main_from_env(self):
        shippostbot.set_cloudwatch(False)
        res = shippostbot.main_from_env()
        self.assertIsInstance(res.get('caption'), str)
        self.assertIsInstance(res.get('comment'), str)
        self.assertIsInstance(res.get('image_url'), str)

    def test_main(self):
        shippostbot.set_cloudwatch(False)
        for selection_type in SelectionType:
            res = shippostbot.main(selection_type, '', '')
            self.assertIsInstance(res.get('caption'), str)
            self.assertIsInstance(res.get('comment'), str)
            self.assertIsInstance(res.get('image_url'), str)

    def test_setup(self):
        os.environ['LOGGING_LEVEL'] = 'ERROR'
        shippostbot.setup_from_env()
        self.assertEqual(shippostbot.log.LOGGING_LEVEL, logging.ERROR)

    def test_cloudwatch(self):
        shippostbot.set_cloudwatch(True)
        self.assertTrue(shippostbot.log.CLOUDWATCH_ENABLED)
