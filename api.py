from flask import Flask, request, current_app as app
from flask_restful import Api, Resource, reqparse
from Application.models import User, Creator, Admin, Song, Album, albumSong, playlist, playlistSong
from Application import config
from Application.database import db
from Application.config import LocalDevelopmentConfig
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    return app

app = create_app()
api = Api(app)

class Songs(Resource):
    def get(self):
        songs = Song.query.all()
        return [song.to_dict() for song in songs]
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int,location='args')
        args = parser.parse_args()
        song = Song.query.filter_by(id=args['id']).first()
        db.session.delete(song)
        db.session.commit()
        songs = Song.query.all()
        return [song.to_dict() for song in songs]
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int,location='args')
        parser.add_argument('name', type=str,location='args')
        parser.add_argument('lyrics', type=str,location='args')
        parser.add_argument('duration', type=int,location='args')
        parser.add_argument('tags', type=str,location='args')
        args = parser.parse_args()
        song = Song.query.filter_by(id=args['id']).first()
        song.name = args['name']
        song.lyrics = args['lyrics']
        song.duration = args['duration']
        song.tags = args['tags']
        db.session.commit()
        songs = Song.query.all()
        return ('Updated', 201)
api.add_resource(Songs, '/songs')
if __name__ == '__main__':
    app.run(debug=True,port=5568)