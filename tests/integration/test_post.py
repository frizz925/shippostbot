import unittest
from typing import List

from shippostbot.entities import Character
from shippostbot.post import select_media_by_characters


class TestPost(unittest.TestCase):
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


def mock_character(*media_ids: List[str]) -> Character:
    return Character(id=None,
                     first_name=None,
                     last_name=None,
                     image_url=None,
                     url=None,
                     media=list(media_ids))


if __name__ == '__main__':
    unittest.main()
