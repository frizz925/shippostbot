import copy
import json
import time
from enum import Enum
from multiprocessing.pool import ThreadPool
from random import Random
from typing import Callable, List, Optional, Tuple, Union

from requests.exceptions import RequestException

from .entities import Character, Media, Post
from .fetchers import (fetch_character, fetch_media, fetch_random_character,
                       fetch_random_media)
from .filter import PostFilter
from .kyoani import fetchers as kyoani_fetchers
from .log import create_logger
from .rng import random_time_based

MAX_FAILURE_RETRY = 3
REQUEST_ERROR_DELAY_IN_MS = 3000

TextProcessor = Callable[[List[Character], List[Media]], str]


class SelectionType(Enum):
    FROM_MEDIA = 0
    FROM_CHARACTERS = 1
    FROM_CHARACTER_TO_MEDIA = 2
    KYOANI_TRIBUTE = 3


def create_post(selection_type: SelectionType,
                caption_fn: Optional[TextProcessor] = None,
                comment_fn: Optional[TextProcessor] = None,
                filter_fn: Optional[PostFilter] = None) -> Post:
    if caption_fn is None:
        caption_fn = create_caption
    if comment_fn is None:
        comment_fn = create_comment

    logger = create_logger(create_post)
    failure = 0
    while True:
        selected_media = None
        selected_charas = None
        try:
            logger.info('Selection type is %s' % selection_type)
            if selection_type is SelectionType.FROM_CHARACTER_TO_MEDIA:
                selected_charas, selected_media = select_character_to_media()
            elif selection_type is SelectionType.FROM_CHARACTERS:
                with ThreadPool(2) as pool:
                    selected_charas = pool.map(lambda x: select_random_character(), range(2))
                selected_media = select_media_by_characters(selected_charas)
            else:
                if selection_type is SelectionType.KYOANI_TRIBUTE:
                    media = kyoani_fetchers.fetch_random_media()
                else:
                    media = fetch_random_media()
                if not validate_media(media):
                    logger.warn('Invalid fetched media: %s' % str(media))
                    continue
                selected_charas, selected_media = select_characters_by_media(media)
        except Exception as e:
            # Fails too many times, just throw the last exception
            if failure >= MAX_FAILURE_RETRY:
                raise e

            if isinstance(e, RequestException):
                delay = REQUEST_ERROR_DELAY_IN_MS
                logger.exception('[Requests] %s. Retrying after %dms' % (str(e), delay))
                time.sleep(delay / 1000)
            else:
                logger.exception('%s. Retrying...' % str(e))
            failure += 1
            continue

        # Since we're doing OTP, there should be at least two characters
        if selected_charas is None or len(selected_charas) < 2:
            logger.info('No suitable characters found. Retrying...')
            continue
        if selected_media is None or len(selected_media) <= 0:
            logger.info('No suitable media found. Retrying...')
            continue

        media = selected_media
        characters = selected_charas
        logger.info('Selected characters: %s' % to_str(characters))
        logger.info('Selected media: %s' % to_str(media))

        caption = caption_fn(characters, media)
        comment = comment_fn(characters, media)
        post = Post(characters=characters,
                    media=media,
                    caption=caption,
                    comment=comment)

        # Update: Filter our posts to avoid containing certain bannable words on some platforms (eg: Facebook)
        if filter_fn is not None and not filter_fn(post):
            logger.info('Post didn\'t pass the filter. Retrying...')
            continue
        return post


def select_character_to_media() -> Tuple[List[Character], List[Media]]:
    random = random_time_based()
    logger = create_logger(select_character_to_media)
    first_chara = select_random_character()
    logger.info('Fetched first character: %s' % to_str(first_chara))

    media_ids = first_chara.media
    if len(media_ids) <= 0:
        raise Exception('Media not found')

    media_id = media_ids.pop(0)
    media = fetch_media(media_id)
    if not validate_media(media):
        raise Exception('Invalid media')
    logger.info('Fetched media: %s' % to_str(media))

    chara_ids = copy.copy(media.characters)
    while len(chara_ids) > 0:
        chara_id = random.choice(chara_ids)
        chara_ids.remove(chara_id)
        # Avoid same character
        if chara_id == first_chara.id:
            continue
        second_chara = fetch_character(chara_id)
        if not validate_character(second_chara):
            continue
        logger.info('Fetched second character: %s' % to_str(second_chara))

        characters = [first_chara, second_chara]
        media = [media]
        return (characters, media)
    raise Exception('Characters not found')


def select_characters_by_media(media: Media) -> Tuple[List[Character], List[Media]]:
    random = random_time_based()
    logger = create_logger(select_characters_by_media)
    if media is None:
        raise Exception('Media not found')
    logger.info('Fetched media: %s' % to_str(media))

    chara_ids = media.characters
    if chara_ids is None:
        raise Exception('Characters not found')

    first_chara = select_and_fetch_character(chara_ids)
    if first_chara is None:
        raise Exception('No suitable character found')

    if first_chara.media[0] != media.id:
        media = fetch_media_by_character(first_chara)
        chara_ids = media.characters
    logger.info('Fetched first character: %s' % to_str(first_chara))

    chara_ids = copy.copy(chara_ids)
    second_chara = None
    while second_chara is None and len(chara_ids) > 0:
        chara_id = random.choice(chara_ids)
        chara_ids.remove(chara_id)
        chara = fetch_character(chara_id)
        if not validate_character(chara):
            continue
        logger.info('Fetched second character: %s' % to_str(chara))
        second_chara = chara

    return ([first_chara, second_chara], [media])


def select_and_fetch_character(chara_ids: List[int],
                               random: Optional[Random] = None) -> Character:
    if random is None:
        random = random_time_based()
    chara_ids = copy.copy(chara_ids)
    while len(chara_ids) > 0:
        chara_id = random.choice(chara_ids)
        chara_ids.remove(chara_id)
        chara = fetch_character(chara_id)
        if not validate_character(chara):
            continue
        return chara
    return None


def select_random_character() -> Character:
    while True:
        chara = fetch_random_character()
        if not validate_character(chara):
            continue
        return chara


def select_media_by_characters(characters: List[Character]) -> List[Media]:
    selected_media = []
    with ThreadPool(len(characters)) as pool:
        selected_media = pool.map(fetch_media_by_character, characters)
    selected_media = [media for media in selected_media if media is not None]
    return selected_media


def fetch_character_by_media(media: Media) -> Character:
    random = random_time_based()
    chara_id = random.choice(media.characters)
    chara = fetch_character(chara_id)
    return chara if validate_character(chara) else None


def fetch_media_by_character(chara: Character) -> Media:
    media_ids = chara.media
    if len(media_ids) <= 0:
        return None
    media_id = media_ids.pop(0)
    media = fetch_media(media_id)
    return media if validate_media(media) else None


def validate_media(media: Media) -> bool:
    if media is None:
        return False
    return True


def validate_character(chara: Character) -> bool:
    if chara is None:
        return False
    # Avoid no images
    image_url = chara.image_url
    if image_url is None or image_url.endswith('default.jpg'):
        return False
    return True


def to_str(obj) -> str:
    return json.dumps(to_dict(obj))


def to_dict(obj) -> dict:
    if isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif isinstance(obj, tuple):
        return obj._asdict()
    return obj


def create_caption(characters: List[Character], media: List[Media] = []) -> str:
    return ' x '.join(create_character_name(chara) for chara in characters)


def create_comment(characters: List[Character], media: List[Media]) -> str:
    comment = "Characters:\r\n" + create_characters_comment(characters)
    comment += "\r\n\r\n"
    comment += "Source(s):\r\n" + create_media_comment(media)
    return comment


def create_characters_comment(characters: List[Character]) -> str:
    return '\r\n'.join(create_character_comment(chara) for chara in characters)


def create_character_comment(character: Character) -> str:
    return '%s: %s' % (create_character_name(character), character.url)


def create_character_name(character: Character) -> str:
    name_parts = [character.last_name, character.first_name]
    name_parts = [name for name in name_parts if name is not None]
    return ' '.join(name_parts).strip()


def create_media_comment(media_list: List[Media]) -> str:
    # HACK: Since our namedtuple is unhashable, we use dict workaround
    media_dict = {}
    for media in media_list:
        media_dict[media.id] = media
    return '\r\n'.join(create_single_media_comment(media) for media in media_dict.values())


def create_single_media_comment(media: Media) -> str:
    return '%s: %s' % (media.title, media.url)


def get_selection_type(selection_type: Union[str, SelectionType]) -> SelectionType:
    if isinstance(selection_type, SelectionType):
        return selection_type
    return getattr(SelectionType, selection_type, SelectionType.FROM_CHARACTER_TO_MEDIA)
