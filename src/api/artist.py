import csv
import sys
import re




class Artist:

    __slots__ = ['__name', '__artistID','__genres']

    def __init__(self, name, artistID, genres):
        self.__name = name
        self.__artistID = artistID
        self.__genres = genres

    def getName(self):
        return self.__name

    def getGenre(self):
        return self.__genre

    def getID(self):
        return self.__artistID
    
    def __repr__(self) -> str:
        return f'\n\
    Name: {self.__name} \n\
    Artist ID: {self.__artistID} \n\
    Primary Genres: {self.__genres} \n'

    