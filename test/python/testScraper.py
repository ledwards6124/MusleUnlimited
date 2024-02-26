import unittest

class testScraper(unittest.TestCase):

    def test_module_load(self):
        self.assertEqual('test'.upper(), 'TEST')
