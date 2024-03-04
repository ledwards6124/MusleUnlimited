import unittest
import os
import sys

cd = os.path.dirname(os.path.abspath(__file__))
srcd = os.path.join(cd, '..', 'src')
sys.path.insert(0, srcd)

from api.music import Artist, Album, Song
from api.spotifyCaller import *

class testMusic(unittest.TestCase):

    def testCoverage(self):
        self.assertEqual('FOO', 'foo'.upper())

    def testArtist(self):
        artist = Artist('MCtesthammer', '1', ['rap'])
        self.assertEqual(artist.getName(), 'MCtesthammer')
        self.assertEqual(artist.getID(), '1')
        self.assertEqual(artist.getGenres(), ['rap'])

    def testSong(self):
        song = Song('trademark usa', '1', Artist('baby keem', '1', ['rap']), [], 250, 1)
        self.assertEqual(song.getName(), 'trademark usa')
        self.assertEqual(song.getID(), '1')
        self.assertFalse(song.getID() == '2')
        self.assertEqual(song.getArtist(), Artist('baby keem', '1', ['rap']))
        self.assertEqual(song.getFeatures(), [])
        self.assertEqual(song.getDuration(), 250)
        self.assertEqual(song.getTrackNum(), 1)

    def testAlbum(self):
        album = Album('the melodic blue', '2',  Artist('baby keem', '1', ['rap']), [],  2021)
        self.assertEqual(album.getName(), 'the melodic blue')
        self.assertEqual(album.getArtist(), Artist('baby keem', '1', ['rap']))
        self.assertEqual(album.getID(), '2')
        self.assertEqual(album.tracks(), [])
        self.assertEqual(album.release(), 2021)
    

