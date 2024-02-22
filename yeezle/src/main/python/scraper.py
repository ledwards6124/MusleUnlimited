from artist import *
import json
from discogs_client import *

TOKEN = 'YXnelCZsMeZmRyIEObnlINawJHiizEjQGUGvJhSN'

def strip(s, char):
    newS = ""
    for ch in s:
        if ch != char:
            newS += ch
    return newS

def connect():
    client = Client('YeezleUnlimited/1.0', user_token=TOKEN)
    return client

def findArtists(name):
    client = connect()
    res = client.search(name, type='artist').page(1)
    artistIDs = {}
    for index in res:
        strIndex = str(index)
        strIndex = str(strip(strIndex, "'"))
        strIndex = str(strip(strIndex, '>'))
        strIndex = str(strIndex[8:])
        indexList = strIndex.split(" ")
        artistID = indexList[0]
        artistName = " ".join([entry for index, entry in enumerate(indexList) if index > 0])
        if artistID not in artistIDs:
            artistIDs[artistID] = artistName
    return artistIDs

def getDiscography(artistID):
    client = connect()
    res = client.artist(artistID).releases.page(1)
    releaseIDs = {}
    for index in res:
        strIndex = str(index)
        strIndex = strip(strIndex, "'")
        strIndex = strIndex[8:]
        strIndex = strip(strIndex, ">")
        indexList = strIndex.split(" ")
        releaseID = indexList[0]
        releaseName = " ".join([entry for index, entry in enumerate(indexList) if index > 0])
        type = index.fetch('type')
        if releaseID not in releaseIDs and type == 'master':
            releaseIDs[releaseID] = releaseName
    return releaseIDs

def getTrackList(albumID):
    client = connect()
    res = client.release(albumID)
    album = []
    i = 0
    for song in res.tracklist:
        strIndex = str(song)
        strIndex = strip(strIndex, "'")
        strIndex = strIndex[7:]
        strIndex = strip(strIndex, ">")
        indexList = strIndex.split(" ")
        trackNum = indexList[0]
        trackName = " ".join([entry for index, entry in enumerate(indexList) if index > 0])
        album.append((trackNum, trackName))
        i += 1
    return album

def getAlbumJSON(albumID):
    client = connect()
    res = client.release(albumID)
    return res.data

res = getTrackList(826492)
for tup in res:
    print(tup)