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

res = getDiscography(3270638)
for val in res:
    print(val, res.get(val))