class Song:

    __slots__ = ['__name', '__songID', '__albumName', '__albumID', '__artist', 
    '__features', '__releaseDate', '__duration' ,'__trackNum']

    def __init__(self, name, songID, artist, features, duration, trackNum):
        self.__name = name
        self.__songID = songID
        self.__artist = artist
        self.__features = features
        self.__duration = duration
        self.__trackNum = trackNum

    def __repr__(self) -> str:
        return f'\n\
    Name: {self.__name} \n\
    ID: {self.__songID} \n\
    Artist: {self.__artist} \n\
    Features {self.__features} \n\
    Duration: {self.__duration} \n\
    Track Number: {self.__trackNum}'

    def getName(self):
        return self.__name

    def getID(self):
        return self.__songID

    def getArtist(self):
        return self.__artist

    def getFeatures(self):
        return self.__features

    def getDuration(self):
        return self.__duration

    def getTrackNum(self):
        return self.__trackNum
    
    def __eq__(self, other):
        if isinstance(other, Song):
            return other.getID() == self.__songID
        return False

class Artist:

    __slots__ = ['__name', '__artistID','__genres']

    def __init__(self, name, artistID, genres):
        self.__name = name
        self.__artistID = artistID
        self.__genres = genres

    def getName(self):
        return self.__name

    def getGenres(self):
        return self.__genres

    def getID(self):
        return self.__artistID

    def __repr__(self) -> str:
        return f'\n\
    Name: {self.__name} \n\
    Artist ID: {self.__artistID} \n\
    Primary Genres: {self.__genres} \n'

    def __eq__(self, other):
        if isinstance(other, Artist):
            return self.__artistID == other.getID()
        return False



class Album:
    __slots__ = ['__name', '__albumID', '__artist', '__songs', '__releaseDate']

    def __init__(self, name, albumID, artist, songs, releaseDate):
        self.__name = name
        self.__albumID = albumID
        self.__artist = artist
        self.__songs = songs
        self.__releaseDate = releaseDate

    def __repr__(self) -> str:
        s = self.__name + f' by {self.__artist.getName()}:\n'
        i = 1
        for t in self.__songs:
            s += f'\t {i} {t.getName()}\n'
            i += 1
        return s

    def getName(self):
        return self.__name

    def getID(self):
        return self.__albumID

    def getArtist(self):
        return self.__artist

    def tracks(self):
        return self.__songs

    def release(self):
        return self.__releaseDate
