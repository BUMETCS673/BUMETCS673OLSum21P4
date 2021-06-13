import unittest
import os
from usda import extract_avg_calorie_data, usda_api_call, load_cfg
from pyprojroot import here

class TestUSDAMethods(unittest.TestCase):

    def test_load_cfg(self):

        self.assertTrue(os.path.isfile(here() / 'user_config.yml'))
        cfg = load_cfg()
        self.assertEqual(type(cfg), dict)
        self.assertIn('usda', cfg.keys())
        self.assertIn('api_key', cfg['usda'].keys())
        self.assertIsNotNone(cfg['usda']['api_key'])

    def test_usda_api_call(self):
        json_response = usda_api_call('apple', load_cfg())


if __name__ == '__main__':
    unittest.main()
