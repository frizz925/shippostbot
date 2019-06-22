import json
import unittest

from click.testing import CliRunner

import shippostbot
from shippostbot.__main__ import main_runner


class TestMain(unittest.TestCase):
    def test_main_runner(self):
        shippostbot.set_cloudwatch(False)
        runner = CliRunner()
        result = runner.invoke(main_runner)
        self.assertEqual(result.exit_code, 0)
        result_json = json.loads(result.output)
        self.assertIsInstance(result_json.get('caption'), str)
        self.assertIsInstance(result_json.get('comment'), str)
        self.assertIsInstance(result_json.get('image_url'), str)


if __name__ == '__main__':
    unittest.main()
