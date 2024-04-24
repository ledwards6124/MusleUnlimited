from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, request
import sys
import os
#sys.path.append(f'{os.path.dirname(os.curdir)}\\..\\api\\')

from spotifyCaller import SpotifyCaller

app = Flask(__name__)
api = Api(app)



class Init(Resource):
    def get(self):
        return c.getToken()
    
class Artist(Resource):
    def get(self):
        name = request.args.get('name')
        id = request.args.get('id')
        if name:
            return c.searchForArtist(name)
        elif id:
            return c.returnArtist(id).toJSON()

class Song(Resource):
        def get(self):
            id = request.args.get('id')
            if id:
                return c.returnSong(id).toJSON()



api.add_resource(Init, '/init')
api.add_resource(Artist, '/artists')
api.add_resource(Song, '/songs')

if __name__ == '__main__':
    c = SpotifyCaller()
    app.run(debug=True)