import unittest
from unittest.mock import Mock

import shippostbot
from shippostbot.post import SelectionType
from shippostbot.social import FacebookPublisher, StreamPublisher
from shippostbot.storage import MemoryStorage


class TestInit(unittest.TestCase):
    def test_main_exception(self):
        def caller():
            shippostbot.create_post = Mock(return_value=None)
            shippostbot.main('FROM_CHARACTER_TO_MEDIA', 'STREAM', 'MEMORY')
        self.assertRaises(Exception, caller)

    def test_get_selection_type(self):
        media_type = SelectionType.FROM_MEDIA
        selection_type = shippostbot.get_selection_type(media_type)
        self.assertEqual(selection_type, media_type)

    def test_get_publisher(self):
        publisher = shippostbot.get_publisher('FACEBOOK', 'AWS_S3')
        self.assertIsInstance(publisher, FacebookPublisher)

        memory_storage = MemoryStorage()
        stream_publisher = StreamPublisher(memory_storage)
        publisher = shippostbot.get_publisher(stream_publisher, memory_storage)
        self.assertEqual(publisher, stream_publisher)

    def test_get_storage(self):
        memory_storage = MemoryStorage()
        storage = shippostbot.get_storage(memory_storage)
        self.assertEqual(storage, memory_storage)


if __name__ == '__main__':
    unittest.main()
