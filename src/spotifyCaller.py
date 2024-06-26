import base64
import requests
import re
import json

ENDPOINT = "https://api.spotify.com/v1"


class SpotifyCaller:
    

    __slots__ = ["__id", "__secret", "__token", "__headers"]

    def __init__(self):
        
        self.__id = "8c825f8af32f4a93a89d1a57a8352a88"
        self.__token = "invalid"
        self.__secret = "4f1a9d94d60245cda6519504004130ca"
        credentials = f"{self.__id}:{self.__secret}"
        credentialsBase64 = base64.b64encode(credentials.encode()).decode()
        self.__headers = {
            "Authorization": f"Basic {credentialsBase64}",
        }
        data = {"grant_type": "client_credentials"}
        response = requests.post(
            "https://accounts.spotify.com/api/token", headers=self.__headers, data=data
        )
        if response.status_code == 200:
            self.__token = response.json().get("access_token")
            self.__headers = {"Authorization": f"Bearer {self.__token}"}

    def __repr__(self) -> str:
        return (
            f"Token: {self.__token}"
            if self.tokenIsValid()
            else "No valid token to display..."
        )

    def getToken(self):
        return self.__token

    def tokenIsValid(self):
        url = f"{ENDPOINT}/artists/3TVXtAsR1Inumwj472S9r4"
        code = requests.get(url, headers=self.__headers)
        return code.status_code == 200

    def getArtist(self, artistID):
        jData = requests.get(f"{ENDPOINT}/artists/{artistID}", headers=self.__headers).json()
        parsed = {
            'name': jData['name'],
            'genres': jData['genres'],
            'id': jData['id']
        }
        return json.dumps(parsed)

    def getAlbum(self, albumID):
        jData = requests.get(f"{ENDPOINT}/albums/{albumID}", headers=self.__headers).json()
        parsed = []
        pattern = r"\s*(?:(feat\.|ft\.|feat|ft|with|\(feat\.|\(ft\.|\(feat|\(ft|\(with))(\s*.*)(\)|\s)$"
        for track in jData['tracks']['items']:
            parsed.append({
            'name': re.sub(pattern, "", track.get("name")),
            'artists': self.__gatherFeatures(track),
            'primary_artist_id': track['artists'][0]['id'],
            'duration': round(track['duration_ms'] / 1000),
            'track': track['track_number']
        })
        return json.dumps(parsed)

    def getTrack(self, songID):
        jData = requests.get(f"{ENDPOINT}/tracks/{songID}", headers=self.__headers).json()
        pattern = r"\s*(?:(feat\.|ft\.|feat|ft|with|\(feat\.|\(ft\.|\(feat|\(ft|\(with))(\s*.*)(\)|\s)$"
        parsed = {
            'name': re.sub(pattern, "", jData["name"]),
            'album': {'name': jData['album']['name'], 'id': jData['album']['id']},
            'artists': self.__gatherFeatures(jData),
            'primary_artist_id': jData['artists'][0]['id'],
            'duration': round(jData['duration_ms'] / 1000),
            'track': jData['track_number']
        }
        return json.dumps(parsed)

    def getTracklist(self, albumID):
        return (
            requests.get(f"{ENDPOINT}/albums/{albumID}/tracks", headers=self.__headers)
            .json()
            .get("items")
        )

    def fetchPopularTracks(self, artistID):
        jData = requests.get(f"{ENDPOINT}/artists/{artistID}/top-tracks", headers=self.__headers).json()
        i = 0
        pattern = r"\s*(?:(feat\.|ft\.|feat|ft|with|\(feat\.|\(ft\.|\(feat|\(ft|\(with))(\s*.*)(\)|\s)$"
        parsed = []
        for d in jData['tracks']:
            if i > 4:
                break
            parsed.append({            
            'name': re.sub(pattern, "", d.get("name")),
            'album': {'name': d['album']['name'], 'id': d['album']['id']},
            'artists': self.__gatherFeatures(d),
            'primary_artist_id': d['artists'][0]['id'],
            'duration': round(d['duration_ms'] / 1000),
            'track': d['track_number']})
            i += 1
        return json.dumps(parsed)
            

    def getAllAlbums(self, artistID):
        albums = []
        response = requests.get(
            f"{ENDPOINT}/artists/{artistID}/albums?include_groups=album",
            headers=self.__headers,
        ).json()
        for tup in response.get("items"):
            albums.append(tup.get("id"))
        return albums

    def returnSong(self, songID):
        songJSON = self.getTrack(songID)
        return self.__parseTrackJSON(songJSON)

    def returnAlbum(self, albumID):
        albumJSON = self.getAlbum(albumID)
        trackJSON = self.getTracklist(albumID)
        albumID = albumJSON.get("id")
        albumName = albumJSON.get("name")
        artist = self.returnArtist(albumJSON.get("artists")[0].get("id"))
        date = albumJSON.get("release_date")[:4]
        tracks = []
        for t in trackJSON:
            tracks.append(self.__parseTrackJSON(t))
        album = Album(albumName, albumID, artist, tracks, date)
        return album

    def returnPopularTracks(self, artistID):
        songs = []
        tracks = self.fetchPopularTracks(artistID)
        for t in tracks.get("tracks"):
            songs.append(self.__parseTrackJSON(t))
        return songs

    def __parseTrackJSON(self, trackJSON):
        pattern = r"\s*(?:(feat\.|ft\.|feat|ft|with|\(feat\.|\(ft\.|\(feat|\(ft|\(with))(\s*.*)(\)|\s)$"
        name = re.sub(pattern, "", trackJSON.get("name"))
        songID = trackJSON.get("id")
        album = trackJSON.get('album')
        if trackJSON.get('album') != None:
            album = trackJSON.get('album').get('name')

        artist = self.returnArtist(trackJSON.get("artists")[0].get("id"))
        features = self.__gatherFeatures(trackJSON)
        duration = round(trackJSON.get("duration_ms") / 1000)
        trackNum = trackJSON.get("track_number")
        return Song(name, songID, artist, features, duration, trackNum, album)

    def __gatherFeatures(self, songJSON):
        artists = songJSON.get("artists")
        count = 0
        features = self.__parseName(songJSON.get("name"))
        for a in artists:
            if count != 0:
                features.add(a.get("name"))
            else:
                count += 1
        return list(features)

    def __parseName(self, songName):
        pattern = r"\s*(?:(feat\.|ft\.|feat|ft|with|\(feat\.|\(ft\.|\(feat|\(ft|\(with))(\s*.*)(\)|\s)$"
        match = re.search(pattern, songName, flags=re.IGNORECASE)
        parsedName = re.sub(pattern, "", songName).strip()
        if match:
            length = len(parsedName)
            regex = rf",\s?|and\s?,?|&\s?|^.{length}"
            features = match.group(2)
            features.replace(parsedName, "")
            featuresList = re.split(regex, features.strip())
            newFeatures = []
            for f in featuresList:
                newFeatures.append(f.strip())
            return set(newFeatures)
        else:
            return set()

    def searchForArtist(self, artistName):
        params = {"q": artistName, "type": "artist"}
        jData = (requests.get(f"{ENDPOINT}/search", headers=self.__headers, params=params).json().get("artists"))
        parsed = []
        i = 0
        for d in jData['items']:
            if i > 4:
                break
            parsed.append({
            'name': d ['name'],
            'genres': d['genres'],
            'id': d['id']
            })
            i += 1
        return parsed
        
        