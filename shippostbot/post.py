import copy
import secrets

from .entities import Anime, Character, Post
from .fetchers import fetch_character, fetch_random_anime
from .log import create_logger

FETCH_ANIME_MAX_RETRY = 5


def create_post() -> Post:
    logger = create_logger('create_post')
    for _ in range(FETCH_ANIME_MAX_RETRY):
        anime = fetch_random_anime()
        if anime is None:
            continue
        logger.info('Fetched anime: %s' % anime)

        chara_nodes = copy.copy(anime['characters']['nodes'])
        if chara_nodes is None:
            continue

        selected_charas = []
        while len(selected_charas) < 2 and len(chara_nodes) > 0:
            chara_node = secrets.choice(chara_nodes)
            chara = fetch_character(chara_node['id'])
            chara_nodes.remove(chara_node)

            if chara is None:
                continue

            # Avoid no images
            image_url = chara['image']['large']
            if image_url is None or image_url.endswith('default.jpg'):
                continue

            selected_charas.append(chara)

        # Since we're doing OTP, there should be at least two characters
        if len(selected_charas) < 2:
            continue
        logger.info('Selected characters: %s' % selected_charas)

        anime = to_anime(anime)
        first_chara = to_character(selected_charas.pop(0))
        second_chara = to_character(selected_charas.pop(0))
        caption = create_caption(anime, first_chara, second_chara)
        return Post(anime=anime,
                    caption=caption,
                    first_character=first_chara,
                    second_character=second_chara)
    return None


def to_anime(anime: dict) -> Anime:
    return Anime(title=anime['title']['userPreferred'])


def to_character(chara: dict) -> Character:
    return Character(first_name=chara['name']['first'],
                     last_name=chara['name']['last'],
                     image_url=chara['image']['large'])


def create_caption(anime: Anime,
                   first_chara: Character,
                   second_chara: Character) -> str:
    first_name = create_character_name(first_chara)
    second_name = create_character_name(second_chara)
    return '%s x %s\r\n(%s)' % (first_name, second_name, anime.title)


def create_character_name(character: Character) -> str:
    name = '%s %s' % (character.last_name, character.first_name)
    return name.strip()
