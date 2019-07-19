import unittest

from shippostbot.entities import Media
from shippostbot.kyoani.fetchers import (fetch_media_page, fetch_media_total,
                                         fetch_random_media)


class TestFetchers(unittest.TestCase):
    def test_fetch_media_total(self):
        total = fetch_media_total()
        self.assertIsInstance(total, int)
        self.assertGreaterEqual(total, 100)

    def test_fetch_media_page(self):
        page = fetch_media_page(1, 10)
        self.assertIsInstance(page, list)
        self.assertEqual(len(page), 10)
        self.assertIn('id', page[0])

    def test_fetch_random_media(self):
        media = fetch_random_media()
        self.assertIsInstance(media, Media)


if __name__ == '__main__':
    unittest.main()
