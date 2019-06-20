import secrets
from collections import namedtuple

import requests

from .entities import Character, Media
from .graphql import Fields, Query, Root
from .log import create_logger

ANILIST_BASE_URL = 'https://graphql.anilist.co'


def fetch_random_media() -> Media:
    return fetch_random(fetch_media_total,
                        fetch_media_page,
                        fetch_media)


def fetch_random_character() -> Character:
    return fetch_random(fetch_character_total,
                        fetch_character_page,
                        fetch_character)


def fetch_random(fn_total, fn_page_fetch, fn_fetch) -> namedtuple:
    total = fn_total()
    page = secrets.randbelow(total)
    node = fn_page_fetch(page, 1).pop()
    return fn_fetch(node['id'])


def fetch_media(media_id: int) -> Media:
    res = fetch('Media', media_id, [
        'id',
        'siteUrl',
        Fields('title', 'userPreferred'),
        Fields('characters', Fields('edges', Fields('node', 'id')))
    ])
    return Media(id=res['id'],
                 url=res['siteUrl'],
                 title=res['title']['userPreferred'],
                 characters=[edge['node']['id'] for edge in res['characters']['edges']])


def fetch_media_total() -> int:
    return fetch_total(Fields('media', 'id'))


def fetch_media_page(page: int, per_page: int) -> list:
    return fetch_page(Fields('media', 'id'), page, per_page)


def fetch_character(chara_id: int) -> Character:
    res = fetch('Character', chara_id, [
        'id',
        'siteUrl',
        Fields('name', ['first', 'last']),
        Fields('image', 'large'),
        Query('media', {
            'page': 1,
            'perPage': 1,
        }, Fields('edges', Fields('node', 'id')))
    ])
    return Character(id=res['id'],
                     first_name=res['name']['first'],
                     last_name=res['name']['last'],
                     image_url=res['image']['large'],
                     url=res['siteUrl'],
                     media=[edge['node']['id'] for edge in res['media']['edges']])


def fetch_character_total() -> int:
    return fetch_total(Fields('characters', 'id'))


def fetch_character_page(page: int, per_page: int) -> list:
    return fetch_page(Fields('characters', 'id'), page, per_page)


def fetch(obj: str, params, fields: list) -> dict:
    logger = create_logger(fetch)
    if not isinstance(params, dict):
        params = {'id': params}
    query = Query(obj, params, fields)
    root = Root(query)
    root_query = str(root)
    logger.debug(root_query)
    result = anilist_query(root_query)
    return result[obj]


def fetch_total(fields: Fields) -> int:
    page = Query('Page', {'page': 1, 'perPage': 1}, [
        Fields('pageInfo', 'total'),
        fields
    ], alias='page')
    root = Root(page)
    result = anilist_query(str(root))
    return result['page']['pageInfo']['total']


def fetch_page(fields: Fields, page: int, per_page: int) -> list:
    page = Query('Page', {'page': page, 'perPage': per_page}, fields, alias='page')
    root = Root(page)
    result = anilist_query(str(root))
    name = fields.name if fields.alias is None else fields.alias
    return result['page'][name]


def anilist_query(query: str, variables: dict = {}) -> dict:
    res = requests.post(ANILIST_BASE_URL, json={
        'query': query, 'variables': variables})
    res.raise_for_status()
    return res.json().get('data', {})
