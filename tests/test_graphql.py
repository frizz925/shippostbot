import sys

from shippostbot.graphql import Field, Fields, Query, Root

EXPECTED_QUERY = '''query($id: Int, $page: Int, $perPage: Int, $search: String) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
      perPage
    }
    media(id: $id, search: $search) {
      id
      title {
        romaji
      }
    }
  }
}'''

EXPECTED_ROOT = '''{
  page: Page(page: 1, perPage: 1) {
    pageInfo {
      total
    }
    media(type: ANIME) {
      id
    }
  }
}'''

EXPECTED_ALIAS = '''{
  Page(page: 1, perPage: 1) {
    Media: media {
      id
      media_title: title
    }
  }
}'''


def test_query():
    page_info = Fields('pageInfo', [
        'total',
        'currentPage',
        'lastPage',
        'hasNextPage',
        'perPage'
    ])
    media = Query('media', {
        'id': '$id',
        'search': '$search'
    }, ['id', Fields('title', 'romaji')])
    page = Query('Page', {
        'page': '$page',
        'perPage': '$perPage'
    }, [page_info, media])
    query = Query('query', {
        '$id': 'Int',
        '$page': 'Int',
        '$perPage': 'Int',
        '$search': 'String'
    }, page)
    assert str(query) == EXPECTED_QUERY


def test_root():
    page = Query('Page', {
        'page': 1,
        'perPage': 1
    }, [
        Fields('pageInfo', 'total'),
        Query('media', {'type': 'ANIME'}, 'id')
    ], alias='page')
    root = Root(page)
    assert str(root) == EXPECTED_ROOT


def test_alias():
    root = Root()
    page = Query('Page', {
        'page': 1,
        'perPage': 1
    }, Fields('media', [
        'id',
        Field('title', 'media_title')
    ], alias='Media'))
    root.add(page)
    assert str(root) == EXPECTED_ALIAS
