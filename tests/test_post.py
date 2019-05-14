from shippostbot.entities import Anime, Character
from shippostbot.post import create_caption, create_character_name


def test_create_character_name():
    # Test with both first and last names
    character = Character(first_name='Akiho',
                          last_name='Senomiya',
                          image_url=None)
    assert create_character_name(character) == 'Senomiya Akiho'

    # Test with only first name
    character = Character(first_name='Haruka',
                          last_name=None,
                          image_url=None)
    assert create_character_name(character) == 'Haruka'

    # Test with only last name
    character = Character(first_name=None,
                          last_name='Misaki',
                          image_url=None)
    assert create_character_name(character) == 'Misaki'


def test_create_caption():
    anime = Anime(title='Darling in the Franxx')
    first_chara = Character(first_name='Hiro',
                            last_name=None,
                            image_url=None)
    second_chara = Character(first_name='Zero Two',
                             last_name=None,
                             image_url=None)
    caption = create_caption(anime, first_chara, second_chara)
    assert caption == 'Hiro x Zero Two\r\n(Darling in the Franxx)'
