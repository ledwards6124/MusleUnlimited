import unittest
from src.api.music import *

class testMusic(unittest.TestCase):

    def testCoverage(self):
        self.assertEqual('FOO', 'foo'.upper())

    def testArtist(self):
        artist = Artist('MCtesthammer', '1', ['rap'])
        self.assertEqual(artist.getName(), 'MCtesthammer')
        self.assertEqual(artist.getID(), '1')
        self.assertEqual(artist.getGenres(), ['rap'])
    

