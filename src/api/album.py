

class Album:
    __slots__ = ['__name', '__albumID', '__artist', '__songs']

    def __init__(self, name, albumID, artist, songs):
        self.__name = name
        self.__albumID = albumID
        self.__artist = artist
        self.__songs = songs

    def __repr__(self) -> str:
        return f'Album Name: {self.__name} \n\
        Album ID: {self.__albumID} \n\
        Artist: {self.__artist} \n\
        Tracklist: {self.__songs}'