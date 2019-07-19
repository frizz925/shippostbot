from typing import List

from ..entities import Media
from ..fetchers import anilist_query, fetch_media, fetch_random
from ..graphql import Fields, Query, Root

KYOANI_STUDIO_ID = 2


def fetch_random_media() -> Media:
    return fetch_random(fetch_media_total,
                        fetch_media_page,
                        fetch_media)


def fetch_media_total() -> int:
    media_query = Query('media',
                        {'page': 1, 'perPage': 1},
                        Fields('pageInfo', 'total'))
    result = query_by_kyoani(media_query)
    return result['media']['pageInfo']['total']


def fetch_media_page(page: int, per_page: int) -> List[dict]:
    media_query = Query('media',
                        {'page': page, 'perPage': per_page},
                        Fields('nodes', 'id'))
    result = query_by_kyoani(media_query)
    return result['media']['nodes']


def query_by_kyoani(fields: Fields) -> dict:
    query = Query('Studio', {'id': KYOANI_STUDIO_ID}, fields)
    root = Root(query)
    result = anilist_query(str(root))
    return result['Studio']
