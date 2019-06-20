from shippostbot.entities import Character, Media
from shippostbot.fetchers import (fetch_character, fetch_media,
                                  fetch_random_character, fetch_random_media)


def test_fetch_media():
    media = fetch_media(21519)
    assert isinstance(media, Media)
    assert media.title == 'Kimi no Na wa.'


def test_fetch_character():
    chara = fetch_character(60153)
    assert isinstance(chara, Character)
    assert chara.first_name == 'Akiho'
    assert chara.last_name == 'Senomiya'


def test_random_media():
    media = fetch_random_media()
    assert isinstance(media, Media)


def test_random_character():
    character = fetch_random_character()
    assert isinstance(character, Character)
