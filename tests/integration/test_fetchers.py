import unittest

from shippostbot.entities import Character, Media
from shippostbot.fetchers import (fetch_character, fetch_media,
                                  fetch_random_character, fetch_random_media)


class TestFetchers(unittest.TestCase):
    def test_fetch_media(self):
        media = fetch_media(21519)
        self.assertIsInstance(media, Media)
        self.assertEqual(media.title, 'Kimi no Na wa.')

    def test_fetch_character(self):
        chara = fetch_character(60153)
        self.assertIsInstance(chara, Character)
        self.assertEqual(chara.first_name, 'Akiho')
        self.assertEqual(chara.last_name, 'Senomiya')

    def test_random_media(self):
        media = fetch_random_media()
        self.assertIsInstance(media, Media)

    def test_random_character(self):
        character = fetch_random_character()
        self.assertIsInstance(character, Character)


if __name__ == '__main__':
    unittest.main()
