import base64
import requests

ENDPOINT = 'https://api.spotify.com/v1'


class Caller:

    __slots__ = ['__id', '__secret', '__token', '__headers']

    def __init__(self):
        self.__id = '8c825f8af32f4a93a89d1a57a8352a88'
        self.__token = 'invalid'
        self.__secret = '4f1a9d94d60245cda6519504004130ca'
        credentials = f"{self.__id}:{self.__secret}"
        credentialsBase64 = base64.b64encode(credentials.encode()).decode()
        self.__headers = {'Authorization':f'Basic {credentialsBase64}',}
        data = {'grant_type':'client_credentials'}
        response = requests.post('https://accounts.spotify.com/api/token', headers=self.__headers, data=data)
        if response.status_code == 200:
            self.__token = response.json().get('access_token')
            self.__headers = {'Authorization': f'Bearer {self.__token}'}

    def getToken(self):
        return self.__token
    
    def tokenIsValid(self):
        url = f'{ENDPOINT}/artists/3TVXtAsR1Inumwj472S9r4'
        code = requests.get(url, headers=self.__headers)
        return code.status_code == 200
    
    def getArtist(self, artistID):
        return requests.get(f'{ENDPOINT}/artists/{artistID}', headers=self.__headers).json()
    
    def getAlbum(self, albumID):
        return requests.get(f'{ENDPOINT}/albums/{albumID}', headers=self.__headers).json()
    
    def getTracklist(self, albumID):
        return requests.get(f'{ENDPOINT}/albums/{albumID}/tracks', headers=self.__headers).json().get('items')
    
    def getAllAlbums(self, artistID):
        albums = []
        response = requests.get(f"{ENDPOINT}/artists/{artistID}/albums?include_groups=album", headers=self.__headers).json()
        for tup in response.get('items'):
            albums.append(tup.get('id'))
        return albums

    def searchForArtist(self, artistName):
        params = {
            'q' : artistName,
            'type': 'artist'
        }
        return requests.get(f'{ENDPOINT}/search', headers=self.__headers, params=params).json().get('artists').get('items')



def main():
    caller = Caller()
    search = caller.searchForArtist('21 savage')
    for tup in search:
        print(tup.get('id'))

main()