import unittest

import sys
import os
sys.path.append(f'{os.path.dirname(os.curdir)}..\\')



from src.music import Artist, Album, Song
from src.spotifyCaller import SpotifyCaller
from src.musle import MusleGame

class testMusic(unittest.TestCase):

    def testCoverage(self):
        self.assertEqual('FOO', 'foo'.upper())

    def testArtist(self):
        artist = Artist('MCtesthammer', '1', ['rap'])
        self.assertEqual(artist.getName(), 'MCtesthammer')
        self.assertEqual(artist.getID(), '1')
        self.assertEqual(artist.getGenres(), ['rap'])

    def testSong(self):
        song = Song('trademark usa', '1', Artist('baby keem', '1', ['rap']), [], 250, 1, 'the melodic blue')
        self.assertEqual(song.getName(), 'trademark usa')
        self.assertEqual(song.getID(), '1')
        self.assertFalse(song.getID() == '2')
        self.assertEqual(song.getArtist(), Artist('baby keem', '1', ['rap']))
        self.assertEqual(song.getFeatures(), [])
        self.assertEqual(song.getDuration(), 250)
        self.assertEqual(song.getTrackNum(), 1)
        self.assertEqual(song.getAlbum(), 'the melodic blue')
    

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
        print('\nCaller Initialized...')
        print(f'Caller Session Token: {self.__caller.getToken()}')

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
        self.assertNotEqual(artistsJSON[1].getID(), '5BwsX8bXOFC1YnqSlyfOKM') #id for red velvet
        self.assertEqual(artistsJSON[0].getID(), '5BwsX8bXOFC1YnqSlyfOKM') #id for redveil
        
    def testPopularTracks(self):
        songs = self.__caller.returnPopularTracks('5K4W6rqBFWDnAN6FQUkS6x')
        names = [s.getName() for s in songs]
        self.assertTrue('CARNIVAL' in names)
        self.assertTrue('I Wonder' in names)
        self.assertTrue('Runaway' in names)
        
class testGame(unittest.TestCase):
    
    __slots__ = ['__game']
    
    def setUp(self):
        print('\nMusle Game Initialized...')
        self.__game = MusleGame('7Hjbimq43OgxaBRpFXic4x') #id for saba
        
    def testInitialization(self):
        self.assertIsInstance(self.__game.solution(), Song)
        #self.assertIsInstance(self.__game.getCaller(), SpotifyCaller)
        self.assertEqual(self.__game.solution().getArtist().getID(), '7Hjbimq43OgxaBRpFXic4x') #very long chain of methods returns artist id, verify that correct artist is chosen
        self.assertEqual(self.__game.getGuessMax(), 8)
        self.assertEqual(self.__game.getGuessTotal(), 0)
        
    def testGameIsValid(self):
        self.assertTrue(self.__game.gameIsValid()) #game is valid since 0 guesses
        for i in range(10):
            self.__game.guess('few good things') #guess more than the limit
        self.assertFalse(self.__game.gameIsValid())
        
    def testGuess(self):
        guess = self.__game.guess('few good things')
        self.assertIsInstance(guess, Song)
        self.assertEqual(guess.getName(), 'Few Good Things')
        self.assertEqual(guess.getArtist().getName(), 'Saba')
        invalidGuess = self.__game.guess('flatbed freestyle') #saba did NOT make this song
        self.assertIsNone(invalidGuess)
        
    def testSolution(self):
        solution = self.__game.solution()
        self.assertTrue(self.__game.songIsSolution(solution))
        notSolution = Song('not solution', '0', 'french montana', [], 69420, 0, 'mac and shit 5')
        self.assertFalse(self.__game.songIsSolution(notSolution))
        
        
    
        
        
        
        




    

    

