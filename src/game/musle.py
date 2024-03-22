import random

from src.api.SpotifyCaller import *


class MusleGame:
    
    __slots__ =['__solutionSong', '__totalGuesses', '__maxGuesses', '__songPool', '__caller']
    
    def __init__(self, artistID):
            self.__caller = SpotifyCaller()
            self.__totalGuesses = 0
            self.__maxGuesses = 8
            self.pickSolutionSong(artistID)
            
    def pickSolutionSong(self, artistID):
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
    
    def gameIsValid(self):
        return self.__totalGuesses <= self.__maxGuesses
    
    def guess(self, guess):
        guess = guess.strip().upper()
        if guess in self.__songPool.keys():
            self.__totalGuesses += 1
            return self.__songPool.get(guess)
        else:
            print(f'{guess} is not a valid song...')
            return None
        
    def songIsSolution(self, song):
        return song == self.__solutionSong        
    
    def scoreGuess(self, guessSong):
        scores = []
        scores.append(self.__scoreYear(guessSong))
        scores.append(self.__scoreTrackNum(guessSong))
        scores.append(self.__scoreDuration(guessSong))
        scores.append(self.__scoreFeatures(guessSong))
        readableScores = []
        for s in scores:
            if s == 0:
                readableScores.append('0')
        
    def scoreYear(self, guessSong):
        res = self.__solutionSong.release() - guessSong.release()
        return res if abs(res) < 5 else 0
    
    def scoreDuration(self, guessSong):
        solutionDuration = self.__solutionSong.getDuration()
        guessDuration = guessSong.getDuration()
        return 1 if abs(solutionDuration - guessDuration) < 30 else 0
    
    def scoreTrackNum(self, guessSong):
        solutionTrack = self.__solutionSong.getTrackNum()
        guessTrack = guessSong.getTrackNum()
        res = solutionTrack - guessTrack
        return res if abs(res) < 4 else 0
    
    def scoreFeatures(self, guessSong):
        solutionFeats = set(self.__solutionSong.getFeatures())
        guessFeatures = set(guessSong.getFeatures())
        crossFeatures = solutionFeats & guessFeatures
        if crossFeatures == guessFeatures:
            return 2
        return 1 if crossFeatures is not None else 0
        
    
    def play(self):
        while self.__gameIsValid():
            guess = input('Enter your guess!\n')
            song = self.__guess(guess)
            if song != None:
                if self.__songIsSolution(song):
                    print('You win!!')
        print(f'The song was {self.__solutionSong}...')

    
        