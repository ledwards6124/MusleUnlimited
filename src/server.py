from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, request
from flask_cors import CORS

from spotifyCaller import SpotifyCaller

app = Flask(__name__)
api = Api(app)
CORS(app)


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
            return c.getArtist(id)

class Song(Resource):
        def get(self):
            id = request.args.get('id')
            popular = request.args.get('popular')
            if id:
                return c.getTrack(id)
            if popular:
                return c.fetchPopularTracks(popular)
            
class Album(Resource):
    def get(self):
        id = request.args.get('id')
        if id:
            return c.getAlbum(id)
        
            
        



api.add_resource(Init, '/init')
api.add_resource(Artist, '/artists')
api.add_resource(Song, '/songs')
api.add_resource(Album, '/albums')

if __name__ == '__main__':
    c = SpotifyCaller()
    app.run(debug=True)