import requests
from flask import Flask, jsonify
import base64
import re
import sqlite3
import json

ENDPOINT = 'https://api.spotify.com/v1'

def getAccessToken():
    clientID = '8c825f8af32f4a93a89d1a57a8352a88'
    clientSecret = '4f1a9d94d60245cda6519504004130ca'
    credentials = f"{clientID}:{clientSecret}"
    credentialsBase64 = base64.b64encode(credentials.encode()).decode()
    headers = {'Authorization':f'Basic {credentialsBase64}',}
    data = {'grant_type':'client_credentials'}
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    if response.status_code == 200:
        return response.status_code, response.json()
    else:
        return response.status_code, response.json()
    
def getArtist(artistID):
    token = getAccessToken()[1].get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{ENDPOINT}/artists/{artistID}", headers=headers)
    return response.status_code, response.json()

def getAlbum(albumID):    
    token = getAccessToken()[1].get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{ENDPOINT}/albums/{albumID}", headers=headers)
    return response.status_code, response.json()

def getDiscography(artistID):
    token = getAccessToken()[1].get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{ENDPOINT}/artists/{artistID}/albums?include_groups=album", headers=headers)
    return response.status_code, response.json()

def getAlbumTracks(albumID):
    token = getAccessToken()[1].get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    tracks = []
    response = requests.get(f"{ENDPOINT}/albums/{albumID}/tracks", headers=headers).json()
    for tup in response.get('items'):
        duration = tup.get('duration_ms') / 1000
        trackID = tup.get('id')
        name = tup.get('name')
        trackNum = tup.get('track_number')
        appearances = tup.get('artists')
        feat2 = []
        for a in appearances:
            feat2.append(a.get('name'))
        parsedName = parseName(name)[0]
        features = parseName(name)[1]        
        tracks.append((trackID, albumID, parsedName, duration, trackNum, combineFeatures(feat2, features)[1:]))
    return tracks

def parseName(songName):
    pattern = r'\s*(?:(feat\.|ft\.|feat|ft|with|\(feat\.|\(ft\.|\(feat|\(ft|\(with))(\s*.*)(\)|\s)$'
    match = re.search(pattern, songName, flags=re.IGNORECASE)
    parsedName = re.sub(pattern, '', songName).strip()
    if match:
        length = len(parsedName)
        regex = rf',\s?|and\s?,?|&\s?|^.{length}'
        features = match.group(2)
        features.replace(parsedName, '')
        featuresList = re.split(regex, features.strip())
        newFeatures = []
        for f in featuresList:
            newFeatures.append(f.strip())
        return parsedName, newFeatures
    else:
        return parsedName, []

def combineFeatures(feat1, feat2):
    allFeatures = []
    for f in feat1:
        allFeatures.append(f)
    for g in feat2:
        if g not in allFeatures:
            allFeatures.append(g)
    return allFeatures

def getDiscographyTuples(artistID):
    response = getDiscography(artistID)[1]
    discography = []
    for tup in response.get('items'):
        albumID = tup.get('id')
        if '(Deluxe)' or '(deluxe)' or 'Deluxe' or 'deluxe' not in tup.get('name'):
            songs = getAlbumTracks(albumID)
            discography += songs
    return discography

def populateSongTable(artistID):
    tuples = getDiscographyTuples(artistID)
    conn = sqlite3.connect('artists.sqlite')
    cur = conn.cursor()
    sql = """
    INSERT INTO songs VALUES
    (?, ?, ?, ?, ?, ?, ?)"""
    inSongs = """
    SELECT name FROM songs
    WHERE name=? AND artist_id=?"""
    for tup in tuples:
        try:
            cur.execute(inSongs, (tup[2], artistID))
            if cur.fetchone() is None:
                cur.execute(sql, (tup[0], artistID, tup[1], tup[3], tup[4], json.dumps(tup[5]), tup[2]))
            else:
                print(f'Failed to add {tup[2]} to song list. Duplicate song...')
        except:
            print(f'Failed to add {tup[2]} to song list. Duplicate song ID: {tup[0]}')
    conn.commit()
    conn.close()
    print('Success!')

def populateArtistsTable():
    sql = """
    SELECT DISTINCT artist_id FROM songs;"""
    insert_sql = """
    INSERT INTO artists VALUES(?, ?)"""
    conn = sqlite3.connect('artists.sqlite')
    cur = conn.cursor()
    cur.execute(sql)
    tuples = cur.fetchall()
    for tup in tuples:
        artistID = tup[0]
        a = getArtist(artistID)[1].get('name')
        cur.execute(insert_sql, (artistID, a))
    conn.commit()
    conn.close()
    print('Success!')

def populateAlbumsTable():
    sql = """
    SELECT DISTINCT album_id FROM songs"""
    insert_sql = """
    INSERT INTO albums VALUES(?, ?)"""
    conn = sqlite3.connect('artists.sqlite')
    cur = conn.cursor()
    cur.execute(sql)
    tuples = cur.fetchall()
    for tup in tuples:
        albumID = tup[0]
        a = getAlbum(albumID)[1].get('name')
        cur.execute(insert_sql, (albumID, a))
    conn.commit()
    conn.close()
    print('Success')

def populateTables(artistIDs):
    conn = sqlite3.connect('artists.sqlite')
    cur = conn.cursor()
    tables = ['artists', 'songs', 'albums']
    for t in tables:
        sql = f"""DELETE FROM {t}"""
        print(f'Wiping table {t}...')
        cur.execute(sql)
    for artistID in artistIDs:
        name = getArtist(artistID)[1].get('name')
        print(f"Retrieving {name}'s Discography...")
        populateSongTable(artistID)
    print('Loading artist information...')
    populateArtistsTable()
    print('Loading album information')
    populateAlbumsTable()
    print('All tables populated!')
    conn.commit()
    conn.close()

    

def main():
    ids = ['3TVXtAsR1Inumwj472S9r4', '5K4W6rqBFWDnAN6FQUkS6x', '4V8LLVI7PbaPR0K2TGSxFF', '6l3HvQ5sa6mXTsMTB19rO5', '0fA0VVWsXO9YnASrzqfmYu']
    populateTables(ids)


main()