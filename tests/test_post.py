import unittest
from typing import List

from shippostbot.entities import Character, Media
from shippostbot.post import (create_caption, create_character_name,
                              create_comment, select_characters_by_media,
                              validate_character)


class TestPost(unittest.TestCase):
    def test_create_character_name(self):
        # Test with both first and last names
        character = Character(id=1,
                              first_name='Akiho',
                              last_name='Senomiya',
                              image_url=None,
                              url='',
                              media=[])
        self.assertEqual(create_character_name(character), 'Senomiya Akiho')

        # Test with only first name
        character = Character(id=2,
                              first_name='Haruka',
                              last_name=None,
                              image_url=None,
                              url='',
                              media=[])
        self.assertEqual(create_character_name(character), 'Haruka')

        # Test with only last name
        character = Character(id=3,
                              first_name=None,
                              last_name='Misaki',
                              image_url=None,
                              url='',
                              media=[])
        self.assertEqual(create_character_name(character), 'Misaki')

    def test_create_caption(self):
        caption = create_caption(create_mock_characters_pair())
        self.assertEqual(caption, 'Hiro x Zero Two')

    def test_create_comment(self):
        media = create_mock_media()
        characters = create_mock_characters_pair()
        comment = create_comment(characters, media)
        expected = '''Characters:
Hiro: https://anilist.co/character/124380/Hiro
Zero Two: https://anilist.co/character/124381/Zero-Two

Source(s):
Darling in the Franxx: https://anilist.co/anime/99423/Darling-in-the-Franxx/'''
        self.assertEqual(comment, expected.replace('\n', '\r\n'))

        # Media with the same titles should only be written once
        media.extend(create_mock_media())
        comment = create_comment(characters, media)
        self.assertEqual(comment, expected.replace('\n', '\r\n'))

    def test_validate_character(self):
        self.assertFalse(validate_character(None))

    def test_select_characters_by_media(self):
        with self.assertRaisesRegex(Exception, 'Media not found'):
            select_characters_by_media(None)
        with self.assertRaisesRegex(Exception, 'Characters not found'):
            media = Media(id='',
                          title='',
                          url='',
                          characters=None)
            select_characters_by_media(media)


def create_mock_characters_pair() -> List[Character]:
    first_chara = Character(id=124380,
                            first_name='Hiro',
                            last_name=None,
                            image_url=None,
                            url='https://anilist.co/character/124380/Hiro',
                            media=[99423])
    second_chara = Character(id=124381,
                             first_name='Zero Two',
                             last_name=None,
                             image_url=None,
                             url='https://anilist.co/character/124381/Zero-Two',
                             media=[99423])
    return [first_chara, second_chara]


def create_mock_media() -> List[Media]:
    media = Media(id=99423,
                  title='Darling in the Franxx',
                  url='https://anilist.co/anime/99423/Darling-in-the-Franxx/',
                  characters=[124380, 124381])
    return [media]


def mock_media(*chara_ids: List[int]) -> Media:
    return Media(id=0,
                 title='Mock Media',
                 url='http://example.org',
                 characters=chara_ids)


if __name__ == '__main__':
    unittest.main()
