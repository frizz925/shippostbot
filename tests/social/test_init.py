import unittest

from shippostbot.social import (FacebookPublisher, Publishers, StreamPublisher,
                                get_publisher)
from shippostbot.storage import MemoryStorage, Storages


class TestInit(unittest.TestCase):
    def test_get_publisher(self):
        publisher = get_publisher('FACEBOOK', 'AWS_S3')
        self.assertIsInstance(publisher, FacebookPublisher)

        publisher = get_publisher(Publishers.FACEBOOK,
                                  Storages.AWS_S3)

        memory_storage = MemoryStorage()
        stream_publisher = StreamPublisher(memory_storage)
        publisher = get_publisher(stream_publisher, memory_storage)
        self.assertEqual(publisher, stream_publisher)


if __name__ == '__main__':
    unittest.main()
