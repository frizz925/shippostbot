from shippostbot.fetchers import fetch_random_character, fetch_random_media


def test_random_media():
    media = fetch_random_media()
    assert isinstance(media, dict)


def test_random_character():
    character = fetch_random_character()
    assert isinstance(character, dict)
