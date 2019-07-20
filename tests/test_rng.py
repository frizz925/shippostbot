import unittest

from shippostbot.rng import random_time_based


class TestRNG(unittest.TestCase):
    def test_random_time_based(self):
        first_random = random_time_based(0)
        second_random = random_time_based(0)
        self.assertEqual(first_random.random(), second_random.random())


if __name__ == '__main__':
    unittest.main()
