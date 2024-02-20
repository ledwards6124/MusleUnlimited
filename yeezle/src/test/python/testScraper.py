import unittest
from python import scraper

class testScraper(unittest.TestCase):

    def test_module_load(self):
        self.assertEqual('test'.upper(), 'TEST')

    
if __name__ == "__main__":
    unittest.main()
