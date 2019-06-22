import unittest
from typing import List

from shippostbot.entities import Character, Media
from shippostbot.post import (create_caption, create_character_name,
                              create_comment, select_media_by_characters)


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

    def test_select_media_by_characters(self):
        characters = [
            mock_character(21355, 104454),
            mock_character(21355),
            mock_character(9253, 10863, 11577)
        ]
        media = select_media_by_characters(characters)
        self.assertEqual(len(media), 3)
        self.assertEqual(media[0].title, 'Re:Zero kara Hajimeru Isekai Seikatsu')
        self.assertEqual(media[1].title, 'Re:Zero kara Hajimeru Isekai Seikatsu')
        self.assertEqual(media[2].title, 'Steins;Gate')


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


def mock_character(*media_ids: List[str]) -> Character:
    return Character(id=None,
                     first_name=None,
                     last_name=None,
                     image_url=None,
                     url=None,
                     media=list(media_ids))


if __name__ == '__main__':
    unittest.main()
