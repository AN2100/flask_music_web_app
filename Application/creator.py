from Application import *
@app.route('/login/creator', methods=['GET', 'POST'])
def creatorLogin():
    return render_template('login.html',form_type = 'Creator login')
@app.route('/login/newcreator', methods=['GET', 'POST'])
def newcreator():
    return render_template('login.html',form_type = 'New Creator Registration')

@app.route('/song/creator/<int:creatorid>/<int:id>/delete', methods=['GET', 'POST'])
def deletecreatorsong(id,creatorid):
    songs = Song.query.all()
    creator = Creator.query.filter_by(id=creatorid).first()
    songdel = Song.query.filter_by(id=id).first()
    # os.remove(os.path.join(curr_dir, songdel.path))
    # os.remove(os.path.join(curr_dir, songdel.image))
    db.session.query(albumSong).filter_by(song_id=id).delete()
    db.session.query(Song).filter_by(id=id).delete()
    db.session.commit()
    users = User.query.all()
    creators = Creator.query.all()
    songs = Song.query.all()
    return render_template('home.html',username=creator.name,type ="creator",songs=songs,id=creator.id)
@app.route('/home/newcreator', methods=['GET', 'POST'])
def newcreatorregister():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        creator = Creator(name=username, password=password,allow=1)
        exist = db.session.query(Creator.id).filter_by(name=username).first()
        if(exist):
            return render_template('registrationResponse.html',response= 'Username already exists please try again with a different username')
        else:
            db.session.add(creator)
            db.session.commit()
            return render_template('registrationResponse.html',response= 'Creator  registered successfully')
        
@app.route('/home/creator', methods=['GET', 'POST'])
def creator():
    songs = Song.query.all()
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        exist = db.session.query(Creator.id).filter_by(name=username,password=password).first()
        if(exist):
            cre = Creator.query.filter_by(id=exist.id).first()
            if(cre.allow == 1):
                return render_template('home.html',username=username,type ="creator",songs=songs,id=exist.id)
            else:
                return render_template('loginResponse.html',response= 'Your account has been blacklisted please contact admin')
        else:
            return render_template('loginResponse.html',response= 'Invalid username or password')
@app.route('/home/creator/<int:id>/add', methods=['GET', 'POST'])
def addform(id):
    return render_template('creators.html',id=id)
@app.route('/home/creator/<int:id>/upload', methods=['GET', 'POST'])
def upload(id):
    if(request.method == 'POST'):
        name = request.form['name']
        music = request.files['filesong']
        thumnail = request.files['fileimg']
        lyrics = request.form['Lyrics']
        duration = request.form['duration']
        artist = request.form['Artist']
        tags = request.form['tags']
        creatorid = id
        parent_dir = os.path.dirname(curr_dir)
        music.save(os.path.join(parent_dir, 'static/Music', music.filename))
        thumnail.save(os.path.join(parent_dir, 'static/Images', thumnail.filename))
        song = Song(name=name, lyrics=lyrics, duration=duration, artist=artist, image=os.path.join('/static/Images', thumnail.filename), path=os.path.join('static/Music', music.filename),tags=tags,rate=0,creatorid=creatorid,count=0)
        exist = db.session.query(Song.id).filter_by(name=name).first()
        if(exist):
            return render_template('uploadResponse.html',response= 'Song already exists please try again with a different song name',id=id)
        else:
            db.session.add(song)
            db.session.commit()
            return render_template('uploadResponse.html',response= 'Song uploaded successfully',id=id)
@app.route('/creator/<int:id>/home', methods=['GET', 'POST'])
def creatorid(id):
    songs = Song.query.all()
    creator = Creator.query.filter_by(id=id).first()
    return render_template('home.html',username=creator.name,type ="creator",songs=songs,id=creator.id)

@app.route('/home/creator/<int:id>/update', methods=['GET', 'POST'])
def albumUpdate(id):
    album = Album.query.filter_by(id=id).first()
    songs = Song.query.filter_by(creatorid=album.creatorid).all()
    return render_template('albumupdate.html',songs=songs,id=id)
@app.route('/album/update/<int:id>', methods=['GET', 'POST'])
def albumupdate(id):
    if(request.method == 'POST'):
        albumname = Album.query.filter_by(id=id).first()
        songs = Song.query.filter_by(creatorid=albumname.creatorid).all()
        name = request.form['name']
        genre = request.form['genre']
        album = Album.query.filter_by(id=id).first()
        album.name = name
        album.genre = genre
        db.session.commit()
        songid=[]
        for song in songs:
            if(request.form[str(song.id)] == 'add' ):
                songid.append(song.id)
        db.session.query(albumSong).filter_by(album_id=id).delete()
        for song in songid:
            albumsongs = albumSong(album_id=id, song_id=song)
            db.session.add(albumsongs)
            db.session.commit()
        return render_template('albumResponse.html',response= 'Album updated successfully',id=album.creatorid)
@app.route('/album/<int:id>/delete', methods=['GET', 'POST'])
def albumdelete(id):
    creator = Album.query.filter_by(id=id).first()
    db.session.query(albumSong).filter_by(album_id=id).delete()
    db.session.query(Album).filter_by(id=id).delete()
    db.session.commit()
    return render_template('albumResponse.html',response= 'Album deleted successfully',id=creator.creatorid)
@app.route('/song/<int:id>/update', methods=['GET', 'POST'])
def songupdate(id):
    if(request.method == 'POST'):
        name = request.form['name']
        lyrics = request.form['Lyrics']
        duration = request.form['duration']
        artist = request.form['Artist']
        tags = request.form['tags']
        song = Song.query.filter_by(id=id).first()
        song.name = name
        song.lyrics = lyrics
        song.duration = duration
        song.artist = artist
        song.tags = tags
        db.session.commit()
        return render_template('uploadResponse.html',response= 'Song updated successfully',id=song.creatorid)
@app.route('/song/creator/<int:id>/edit')
def editsong(id):
    return render_template('songupdate.html',id=id)
@app.route('/creator/<int:creatorID>/song/<int:id>/delete', methods=['GET', 'POST'])
def creatorUpdate(creatorID,id):
    db.session.query(albumSong).filter_by(song_id=id).delete()
    db.session.query(Song).filter_by(id=id).delete()
    db.session.commit()
    songs = Song.query.all()
    creator = Creator.query.filter_by(id=creatorID).first()
    return render_template('home.html',username=creator.name,type ="creator",songs=songs,id=creator.id)
@app.route('/album/<int:id>/add', methods=['GET', 'POST'])
def albumadd(id):
    songs = Song.query.filter_by(creatorid=id).all()
    creator=Creator.query.filter_by(id=id).first()
    return render_template('albumcreation.html',songs=songs,id=id)
@app.route('/home/creator/<int:id>/newalbum', methods=['GET', 'POST'])
def addAlbum(id):
    if(request.method == 'POST'):
        songs = Song.query.filter_by(creatorid=id).all()
        creator=Creator.query.filter_by(id=id).first()
        name = request.form['name']
        genre = request.form['genre']
        songid=[]
        for song in songs:
            if(request.form[str(song.id)] == 'add' ):
                songid.append(song.id)
        album = Album(name=name, artist=creator.name, genre=genre,creatorid=id)
        exist = db.session.query(Album.id).filter_by(name=name).first()
        if(exist):
            return render_template('albumResponse.html',response= 'Album already exists please try again with a different album name',id=id)
        else:
            db.session.add(album)
            db.session.commit()
            album = Album.query.filter_by(name=name).first()
            for song in songid:
                albumsong = albumSong(album_id=album.id, song_id=song)
                db.session.add(albumsong)
                db.session.commit()
            return render_template('albumResponse.html',response= 'Album created successfully',id=id)