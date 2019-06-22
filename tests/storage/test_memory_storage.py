import unittest

from shippostbot.storage import MemoryStorage


class TestMemoryStorage(unittest.TestCase):
    def test_memory_storage(self):
        content_name = 'mock-content'
        content_type = 'application/octet-stream'
        mock_content = b''

        storage = MemoryStorage()
        f = storage.save(content_name, mock_content, content_type)
        self.assertEqual(storage.read(content_name), mock_content)
        self.assertEqual(f.content_type, content_type)
        self.assertEqual(f.content, mock_content)
        self.assertEqual(f.name, content_name)

        new_content = b'000000'
        f = f.save(new_content)
        self.assertEqual(f.content, new_content)

        f.delete()
        self.assertIsNone(storage.read(content_name))


if __name__ == '__main__':
    unittest.main()
