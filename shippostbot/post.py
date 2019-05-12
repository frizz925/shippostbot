import copy
import logging
import secrets

from .entities import Anime, Character, Post
from .fetchers import fetch_character, fetch_random_anime

FETCH_ANIME_MAX_RETRY = 5


def create_post() -> Post:
    for _ in range(FETCH_ANIME_MAX_RETRY):
        anime = fetch_random_anime()
        if anime is None:
            continue
        logging.info('Fetched anime: %s' % anime)

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
        logging.info('Selected characters: %s' % selected_charas)

        anime = to_anime(anime)
        first_character = to_character(selected_charas.pop())
        second_character = to_character(selected_charas.pop())
        return Post(anime=anime,
                    first_character=first_character,
                    second_character=second_character)
    return None


def to_anime(anime: dict) -> Anime:
    return Anime(title=anime['title']['userPreferred'])


def to_character(chara: dict) -> Character:
    return Character(first_name=chara['name']['first'],
                     last_name=chara['name']['last'],
                     image_url=chara['image']['large'])
