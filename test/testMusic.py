import unittest
import os
import sys

cd = os.path.dirname(os.path.abspath(__file__))
srcd = os.path.join(cd, '..', 'src')
sys.path.insert(0, srcd)

from src.api.music import Artist

class testMusic(unittest.TestCase):

    def testCoverage(self):
        self.assertEqual('FOO', 'foo'.upper())

    def testArtist(self):
        artist = Artist('MCtesthammer', '1', ['rap'])
        self.assertEqual(artist.getName(), 'MCtesthammer')
        self.assertEqual(artist.getID(), '1')
        self.assertEqual(artist.getGenres(), ['rap'])
    

