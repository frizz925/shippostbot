import copy
import secrets

from .entities import Character, Media, Post
from .fetchers import fetch_character, fetch_random_media
from .log import create_logger


def create_anime_post() -> Post:
    logger = create_logger(create_anime_post)
    while True:
        media = fetch_random_media()
        if media is None:
            logger.info('Media not found. Retrying...')
            continue
        logger.info('Fetched media: %s' % media)

        chara_nodes = copy.copy(media['characters']['nodes'])
        if chara_nodes is None:
            logger.info('Characters not found. Retrying...')
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
            logger.info('No suitable characters found. Retrying...')
            continue
        logger.info('Selected characters: %s' % selected_charas)

        media = to_media(media)
        first_chara = to_character(selected_charas.pop(0))
        second_chara = to_character(selected_charas.pop(0))
        caption = create_caption(media, first_chara, second_chara)
        return Post(media=media,
                    caption=caption,
                    first_character=first_chara,
                    second_character=second_chara)


def to_media(media: dict) -> Media:
    return Media(title=media['title']['userPreferred'])


def to_character(chara: dict) -> Character:
    return Character(first_name=chara['name']['first'],
                     last_name=chara['name']['last'],
                     image_url=chara['image']['large'])


def create_caption(media: Media,
                   first_chara: Character,
                   second_chara: Character) -> str:
    first_name = create_character_name(first_chara)
    second_name = create_character_name(second_chara)
    return '%s x %s\r\n(%s)' % (first_name, second_name, media.title)


def create_character_name(character: Character) -> str:
    name_parts = [character.last_name, character.first_name]
    name_parts = [name for name in name_parts if name is not None]
    return ' '.join(name_parts).strip()
