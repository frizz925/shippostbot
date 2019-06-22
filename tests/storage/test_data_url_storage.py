import unittest

from shippostbot.storage import DataUrlStorage


class TestDataUrlStorage(unittest.TestCase):
    def test_storage(self):
        storage = DataUrlStorage()
        self.assertTrue(storage.is_public)
        self.assertRaises(NotImplementedError, lambda: storage.read(''))
        storage.delete('')

        f = storage.save('kek', b'')
        self.assertEqual(f.content, b'')
        self.assertEqual(f.public_url, 'data:application/octet-stream;base64,')

        content_type = f.content_type
        f = f.save(b'000')
        self.assertEqual(f.content, b'000')
        self.assertEqual(f.content_type, content_type)
        f.delete()


if __name__ == '__main__':
    unittest.main()
