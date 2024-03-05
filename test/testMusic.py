import unittest
import os
import sys

cd = os.path.dirname(os.path.abspath(__file__))
srcd = os.path.join(cd, '..', 'src')
sys.path.append(srcd)

from src.api.music import Artist, Album, Song
from src.api.SpotifyCaller import *

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

class testAPI(unittest.TestCase):

    __slots__ = ['__caller']

    def setUp(self):
        self.__caller = SpotifyCaller()
        print('\nCaller Initialized\t')

    def testTokenExists(self):
        self.assertIsNotNone(self.__caller.getToken())

    def testTokenIsValid(self):
        self.assertTrue(self.__caller.tokenIsValid())        

    def testGetArtist(self):
        artistJSON = self.__caller.getArtist('5K4W6rqBFWDnAN6FQUkS6x') #id for kanye west
        self.assertEqual(artistJSON.get('name'), 'Kanye West')
        self.assertEqual(artistJSON.get('id'), '5K4W6rqBFWDnAN6FQUkS6x')

    def testGetAlbum(self):
        albumJSON = self.__caller.getAlbum('30zwjSQEodaUXCn11nmiVF') #id for vultures 1
        self.assertEqual(albumJSON.get('name'), 'VULTURES 1')
        self.assertEqual(albumJSON.get('id'), '30zwjSQEodaUXCn11nmiVF')
        self.assertEqual(albumJSON.get('artists')[1].get('name'), 'Kanye West')

    def testGetSong(self):
        songJSON = self.__caller.getTrack('3w0w2T288dec0mgeZZqoNN') #id for carnival
        self.assertEqual(songJSON.get('name'), 'CARNIVAL')
        self.assertEqual(songJSON.get('id'), '3w0w2T288dec0mgeZZqoNN')
        self.assertEqual(songJSON.get('track_number'), 12)
        self.assertEqual(songJSON.get('artists')[2].get('name'), 'Ty Dolla $ign')

    def testGetTracklist(self):
        trackList = self.__caller.getTracklist('30zwjSQEodaUXCn11nmiVF') #id for vultures 1
        self.assertEqual(len(trackList), 16)
        self.assertEqual(trackList[11].get('name'), 'CARNIVAL') 
        self.assertEqual(trackList[0].get('id'), '347AQK5Lyhn6RvB8tBGYxt') #id for 'STARS'

    def testGetAllAlbums(self):
        albums = self.__caller.getAllAlbums('5K4W6rqBFWDnAN6FQUkS6x') #id for kanye west
        self.assertEqual(albums[0], '30zwjSQEodaUXCn11nmiVF') #id for vultues 1
        self.assertEqual(albums[4],'6pwuKxMUkNg673KETsXPUV') #id for kids see ghosts
        self.assertEqual(albums[6], '7gsWAHLeT0w7es6FofOXk1') #id for the life of pablo

    def testReturnSong(self):
        song = self.__caller.returnSong('6AshXllQhobwSXsdpgp41w') #id for johnny ps caddy
        self.assertIsInstance(song, Song)
        self.assertEqual(song.getName(), "Johnny P's Caddy")
        self.assertEqual(song.getFeatures(), ['J. Cole'])

    def testReturnArtist(self):
        artist = self.__caller.returnArtist('6l3HvQ5sa6mXTsMTB19rO5') #id for jcole
        self.assertIsInstance(artist, Artist)
        self.assertEqual(artist.getName(), 'J. Cole')
        self.assertEqual(artist.getID(), '6l3HvQ5sa6mXTsMTB19rO5')

    def testReturnAlbum(self):
        album = self.__caller.returnAlbum('4dhK1XKetMnAilmo6CMID8') #id for few good things
        self.assertIsInstance(album, Album)
        self.assertIsInstance(album.getArtist(), Artist)
        self.assertEqual(album.getArtist().getName(), 'Saba')
        self.assertEqual(album.release(), '2022')
        trackNum = 1
        for song in album.tracks():
            self.assertIsInstance(song, Song)
            self.assertEqual(song.getTrackNum(), trackNum)
            trackNum += 1

    def testArtistSearch(self):
        artistsJSON = self.__caller.searchForArtist('redveil')
        self.assertEqual(artistsJSON[0].getName(), 'redveil')
        self.assertEqual(artistsJSON[1].getID(), '6yJ6QQ3Y5l0s0tn7b0arrO') #id for red velvet
        self.assertEqual(artistsJSON[0].getID(), '5BwsX8bXOFC1YnqSlyfOKM') #id for redveil
        
        




    

    

