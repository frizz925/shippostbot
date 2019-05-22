from shippostbot.fetchers import (fetch_character, fetch_media,
                                  fetch_random_character, fetch_random_media)


def test_fetch_media():
    media = fetch_media(21519)
    assert isinstance(media, dict)
    assert media['title']['userPreferred'] == 'Kimi no Na wa.'


def test_fetch_character():
    chara = fetch_character(60153)
    assert isinstance(chara, dict)
    assert chara['name']['last'] == 'Senomiya'
    assert chara['name']['first'] == 'Akiho'


def test_random_media():
    media = fetch_random_media()
    assert isinstance(media, dict)


def test_random_character():
    character = fetch_random_character()
    assert isinstance(character, dict)
