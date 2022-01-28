import unittest

from shippostbot.entities import Post
from shippostbot.filter.file_filter import file_filter


class TestFileFilter(unittest.TestCase):
    def test_file_filter(self):
        self.assertFalse(file_filter(Post(
            caption='Adolf Hitler caption',
            comment='Adolf Hitler comment',
        )))

        self.assertFalse(file_filter(Post(
            caption='Harmless caption',
            comment='Adolf Hitler comment',
        )))

        self.assertFalse(file_filter(Post(
            caption='Adolf Hitler caption',
            comment='Harmless comment',
        )))

        self.assertTrue(file_filter(Post(
            caption='Harmless caption',
            comment='Harmless comment',
        )))
