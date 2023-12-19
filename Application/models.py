from .database import db
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
class Creator(db.Model):
    __tablename__ = 'creator'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    allow = db.Column(db.Integer)
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    lyrics = db.Column(db.String)
    duration = db.Column(db.Integer)
    path = db.Column(db.String)
    artist = db.Column(db.String)
    image = db.Column(db.String)
    tags = db.Column(db.String)
    rate = db.Column(db.Integer)
    count = db.Column(db.Integer)
    creatorid = db.Column(db.Integer, db.ForeignKey('creator.id'))
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    artist = db.Column(db.String)
    genre = db.Column(db.String)
    creatorid = db.Column(db.Integer, db.ForeignKey('creator.id', ondelete='CASCADE'))
class albumSong(db.Model):
    __tablename__ = 'album-sond'
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id', ondelete='CASCADE'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id', ondelete='CASCADE'))
class playlist(db.Model):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    userid = db.Column(db.Integer, db.ForeignKey('creator.id', ondelete='CASCADE'))
class playlistSong(db.Model):
    __tablename__ = 'playlist_song'
    id = db.Column(db.Integer, primary_key=True)
    playlistid = db.Column(db.Integer, db.ForeignKey('playlist.id', ondelete='CASCADE'))
    songid = db.Column(db.Integer, db.ForeignKey('song.id', ondelete='CASCADE'))