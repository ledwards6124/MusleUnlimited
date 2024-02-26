import base64
import requests

ENDPOINT = 'https://api.spotify.com/v1'


class Caller:

    __slots__ = ['__id', '__secret', '__token', '__headers'], 

    def __init__(self):
        self.__id = '8c825f8af32f4a93a89d1a57a8352a88'
        self.__token = 'invalid'
        self.__secret = '4f1a9d94d60245cda6519504004130ca'
        credentials = f"{self.__id}:{self.__secret}"
        credentialsBase64 = base64.b64encode(credentials.encode()).decode()
        self.__headers = {'Authorization':f'Basic {self.__credentialsBase64}',}
        data = {'grant_type':'client_credentials'}
        response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
        if response.status_code == 200:
            self.__token = response.json().get('access_token')

    def getToken(self):
        return self.__token
    
    def tokenIsValid(self):

def main():

    caller = Caller()
    print(caller.getToken())

main()