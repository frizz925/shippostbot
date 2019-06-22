import unittest

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


class TestGraphQL(unittest.TestCase):
    def test_query(self):
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
        self.assertEqual(str(query), EXPECTED_QUERY)

    def test_root(self):
        page = Query('Page', {
            'page': 1,
            'perPage': 1
        }, [
            Fields('pageInfo', 'total'),
            Query('media', {'type': 'ANIME'}, 'id')
        ], alias='page')
        root = Root(page)
        self.assertEqual(str(root), EXPECTED_ROOT)

    def test_alias(self):
        root = Root()
        page = Query('Page', {
            'page': 1,
            'perPage': 1
        }, Fields('media', [
            'id',
            Field('title', 'media_title')
        ], alias='Media'))
        root.add(page)
        self.assertEqual(str(root), EXPECTED_ALIAS)


if __name__ == '__main__':
    unittest.main()
