import secrets

import requests

ANILIST_BASE_URL = 'https://graphql.anilist.co'


def fetch_random_anime():
    total = fetch_anime_total()
    page = secrets.randbelow(total)
    anime_node = fetch_anime_page(page, 1).pop()
    anime = fetch_anime(anime_node['id'])
    return anime


def fetch_anime(anime_id: int) -> dict:
    result = anilist_query('''query($id: Int) {
        media: Media(id: $id, type: ANIME) {
            id
            title { userPreferred }
            characters {
                nodes { id }
            }
        }
    }''', {'id': anime_id})
    return result['media']


def fetch_anime_total() -> int:
    result = anilist_query('''{
        page: Page(page: 1, perPage: 1) {
            pageInfo { total }
            media(type: ANIME) { id }
        }
    }''')
    return result['page']['pageInfo']['total']


def fetch_anime_page(page: int, per_page: int) -> list:
    result = anilist_query('''query($page: Int, $perPage: Int) {
        page: Page(page: $page, perPage: $perPage) {
            media(type: ANIME) { id }
        }
    }''', {'page': page, 'perPage': per_page})
    return result['page']['media']


def fetch_character(chara_id: int) -> dict:
    result = anilist_query('''query($id: Int) {
        character: Character(id: $id) {
            id
            name {
                first
                last
            }
            image {
                large
            }
        }
    }''', {'id': chara_id})
    return result['character']


def anilist_query(query: str, variables: dict = {}) -> dict:
    res = requests.post(ANILIST_BASE_URL, json={
                        'query': query, 'variables': variables})
    return res.json().get('data', {})
