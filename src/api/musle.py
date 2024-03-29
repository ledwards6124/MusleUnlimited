import random

import sys
import os
sys.path.append(f'{os.path.dirname(os.curdir)}..\\src\\api\\')

from .SpotifyCaller import *


class MusleGame:
    
    __slots__ =['__solutionSong', '__totalGuesses', '__maxGuesses', '__songPool', '__caller', '__scores', '__albumYears']
    
    def __init__(self, artistID):
            self.__caller = SpotifyCaller()
            self.__totalGuesses = 0
            self.__maxGuesses = 8
            self.__scores = [[]]
            self.pickSolutionSong(artistID)
            
    def pickSolutionSong(self, artistID):
        albumIDs = self.__caller.getAllAlbums(artistID)
        self.__songPool = {}
        self.__albumYears = {}
        for id in albumIDs:
            album = self.__caller.returnAlbum(id)
            if album.release() not in self.__albumYears.keys():
                self.__albumYears[album.release()] = album.tracks()
            for song in album.tracks():
                self.__songPool[song.getName().upper()] = song            
        self.__solutionSong = random.choice(list(self.__songPool.values()))
        
    def solution(self):
        return self.__solutionSong
    
    def getYears(self):
        return self.__albumYears
    
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
        self.__scores[0].append(self.scoreYear(guessSong))
        self.__scores[0].append(self.scoreTrackNum(guessSong))
        self.__scores[0].append(self.scoreDuration(guessSong))
        self.__scores[0].append(self.scoreFeatures(guessSong))
        print(self.stringifyScores())

    def stringifyScores(self):
        scoreString = f'Previous Guesses in {self.solution().getArtist().getName()}''s Discography:\n'
        categories = 'Release Year | Track Number | Duration | Features\n'
        scoreString += categories
        for s in self.__scores:
            idx = 0
            line = ''
            while idx < 4:
                currScore = self.__scores[s][idx]
                newScore = ''
                if currScore == 0:
                    newScore = 'O'
                elif currScore == 1:
                    newScore = '/\\'
                elif currScore == -1:
                    newScore = 'V'
                elif currScore == 2:
                    newScore = 'X'
                else:
                    newScore = '?'
                if idx == 3:
                    line += f'    {newScore}    |'
                else:
                    line += f'    {newScore}\n'
                idx += 1

                
        
    def scoreYear(self, guessSong):
        currYear = 0
        solYear = 1
        for year in self.__albumYears.keys():
            for song in self.__albumYears[year]:
                if song.getName() == guessSong.getName():
                    currYear = year
                if song.getName() == self.solution.getName():
                    solYear = year

        if currYear == solYear:
            return 2
        return 1 if abs(currYear - solYear) < 5 else 0
                
    
    def scoreDuration(self, guessSong):
        solutionDuration = self.__solutionSong.getDuration()
        guessDuration = guessSong.getDuration()
        if solutionDuration == guessDuration:
            return 2
        return 1 if abs(solutionDuration - guessDuration) < 30 else 0
    
    def scoreTrackNum(self, guessSong):
        solutionTrack = self.__solutionSong.getTrackNum()
        guessTrack = guessSong.getTrackNum()
        res = solutionTrack - guessTrack
        if res == 0:
            return 2
        elif abs(res) < 3:
            return res
        return 0
    
    def scoreFeatures(self, guessSong):
        solutionFeats = set(self.__solutionSong.getFeatures())
        guessFeatures = set(guessSong.getFeatures())
        crossFeatures = solutionFeats & guessFeatures
        if crossFeatures == guessFeatures:
            return 2
        return 1 if crossFeatures is not None else 0
        
    
    def play(self):
        while self.gameIsValid():
            guess = input('Enter your guess!\n')
            song = self.guess(guess)
            if song != None:
                self.scoreGuess(song)
                if self.songIsSolution(song):
                    print('You win!!')
        print(f'The song was {self.__solutionSong}...')

    
        