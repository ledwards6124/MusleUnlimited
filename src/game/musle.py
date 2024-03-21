import random

from api.SpotifyCaller import *


class MusleGame:
    
    __slots__ =['__solutionSong', '__totalGuesses', '__maxGuesses', '__songPool', '__caller']
    
    def __init__(self, artistID):
            self.__caller = SpotifyCaller()
            self.__totalGuesses = 0
            self.__maxGuesses = 8
            self.__pickSolutionSong(artistID)
            self.__albumNums = {}
            
    def __pickSolutionSong(self, artistID):
        albumIDs = self.__caller.getAllAlbums(artistID)
        self.__songPool = {}
        albumYears = {}
        for id in albumIDs:
            album = self.__caller.returnAlbum(id)
            if album.release() not in albumYears.keys():
                albumYears[album.release()] = album.getName()
            for song in album.tracks():
                self.__songPool[song.getName().upper()] = song            
        self.__solutionSong = random.choice(list(self.__songPool.values()))
        
    def solution(self):
        return self.__solutionSong
    
    def getGuessTotal(self):
        return self.__totalGuesses
    
    def getGuessMax(self):
        return self.__maxGuesses
    
    def getCaller(self):
        return self.__caller
    
    def __gameIsValid(self):
        return self.__totalGuesses <= self.__maxGuesses
    
    def __guess(self, guess):
        guess = guess.strip().upper()
        if guess in self.__songPool.keys():
            self.__totalGuesses += 1
            return self.__songPool.get(guess)
        else:
            print(f'{guess} is not a valid song...')
            return None
        
    def __songIsSolution(self, song):
        return song == self.__solutionSong        
    
    def __scoreGuess(self, guessSong):
        pass
        
    def __scoreYear(self, guessSong):
        res = self.__solutionSong.release() - guessSong.release()
        return res if abs(res) < 5 else 0
    
    def __scoreDuration(self, guessSong):
        res = self.__solutionSong
        
    
    def play(self):
        while self.__gameIsValid():
            guess = input('Enter your guess!\n')
            song = self.__guess(guess)
            if song != None:
                if self.__songIsSolution(song):
                    print('You win!!')
        print(f'The song was {self.__solutionSong}...')

    
        