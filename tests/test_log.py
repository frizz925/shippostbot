import unittest

from shippostbot.log import create_logger


class TestLog(unittest.TestCase):
    def test_create_logger(self):
        logger = create_logger(TestLog)
        self.assertEqual(logger.name, TestLog.__name__)
        logger = create_logger(self)
        self.assertEqual(logger.name, TestLog.__name__)
        logger = create_logger('test_logger')
        self.assertEqual(logger.name, 'test_logger')


if __name__ == '__main__':
    unittest.main()
