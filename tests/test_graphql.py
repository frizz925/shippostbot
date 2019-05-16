import sys

from shippostbot.graphql import Field, Fields, Query

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
