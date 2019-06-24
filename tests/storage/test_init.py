import unittest

from shippostbot.storage import MemoryStorage, get_storage


class TestInit(unittest.TestCase):
    def test_get_storage(self):
        memory_storage = MemoryStorage()
        storage = get_storage(memory_storage)
        self.assertEqual(storage, memory_storage)


if __name__ == '__main__':
    unittest.main()
