import re

class Song:

    __slots__ = ['__name', '__songID', '__albumName', '__albumID', '__artistName', '__artistID', '__features', '__releaseDate', '__duration']

    def __init__(self, name, songID, albumName, albumID, artistName, artistID, features, releaseDate, duration):
        self.__name = name
        self.__songID = songID
        self.__albumName = albumName
        self.__albumID = albumID
        self.__artistName = artistName
        self.__artistID = artistID
        self.__features = features
        self.__releaseDate = releaseDate
        self.__duration = duration

    def __repr__(self) -> str:
        return f'\n\
    Name: {self.__name} \n\
    ID: {self.__songID} \n\
    Album Name: {self.__albumName} \n\
    Album ID: {self.__albumID} \n\
    Artist Name: {self.__artistName} \n\
    Artist ID: {self.__artistID} \n\
    Features {self.__features} \n\
    Release Date: {self.__releaseDate} \n\
    Duration: {self.__duration} \n'




