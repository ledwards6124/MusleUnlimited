import requests
from flask import Flask, jsonify
import base64

app = Flask(__name__)

ENDPOINT = 'https://api.spotify.com/v1'

@app.route('/get_token', methods=['POST'])
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
    
@app.route('/artists/<artist_id>', methods=['GET'])
def getArtist(artistID):
    token = getAccessToken()[1].get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{ENDPOINT}/artists/{artistID}", headers=headers)
    return response.status_code, response.json()

@app.route('/albums/<albumID>', methods=['GET'])
def getAlbum(albumID):    
    token = getAccessToken()[1].get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{ENDPOINT}/albums/{albumID}", headers=headers)
    return response.status_code, response.json()

@app.route('/albums/<artistID>/albums')
def getDiscography(artistID):
    token = getAccessToken()[1].get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{ENDPOINT}/artists/{artistID}/albums?include_groups=album", headers=headers)
    return response.status_code, response.json()

@app.route('/albums/<albumID>/tracks')
def getAlbumTracks(albumID):
    token = getAccessToken()[1].get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    tracks = []
    response = requests.get(f"{ENDPOINT}/albums/{albumID}/tracks", headers=headers).json()
    for tup in response.get('items'):
        duration = tup.get('duration_ms') / 1000
        trackID = tup.get('id')
        name = tup.get('name')
        tracks.append((name, trackID, duration))
    return tracks
def main():
    res = getDiscography('3qiHUAX7zY4Qnjx8TNUzVx')
    for tup in res[1].get('items'):
        albumID = tup.get('id')
        tracks = getAlbumTracks(albumID)
        for track in tracks:
            print(track)

main()