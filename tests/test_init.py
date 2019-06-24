import unittest
from unittest.mock import Mock

import shippostbot


class TestInit(unittest.TestCase):
    def test_main_exception(self):
        def caller():
            shippostbot.create_post = Mock(return_value=None)
            shippostbot.main('FROM_CHARACTER_TO_MEDIA', 'STREAM', 'MEMORY')
        self.assertRaises(Exception, caller)


if __name__ == '__main__':
    unittest.main()
