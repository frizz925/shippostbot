import unittest

from shippostbot.storage import MemoryStorage, TempStorage


class TestTempStorage(unittest.TestCase):
    def test_storage(self):
        mem_storage = MemoryStorage()
        tmp_storage = TempStorage()

        content = 'Hello, world!'.encode()
        content_type = 'text/plain'
        f = mem_storage.save('keksimus', content, content_type)
        f = f.save_to_storage(tmp_storage)
        self.assertIsInstance(f.path, str)
        self.assertEqual(f.content, content)
        self.assertEqual(f.public_url, 'file://' + f.path)

        f.delete_from_storage(mem_storage)
        self.assertIsNone(mem_storage.read(f.name))


if __name__ == '__main__':
    unittest.main()
