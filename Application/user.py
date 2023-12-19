from Application import *
@app.route('/login/user', methods=['GET', 'POST'])
def userLogin():
    return render_template('login.html',form_type = 'User login')

@app.route('/login/newuser', methods=['GET', 'POST'])
def newuser():
    return render_template('login.html',form_type = 'New User Registration')

@app.route('/songs/<int:id>', methods=['GET', 'POST'])
def creatorSongs(id):
    songs = Song.query.filter_by(creatorid=id).all()
    creator = Creator.query.filter_by(id=id).first()
    return render_template('songs.html',songs=songs,name=creator.name,creatorid=creator.id)

@app.route('/home/newuser', methods=['GET', 'POST'])
def newuserregister():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        user = User(name=username, password=password)
        exist = db.session.query(User.id).filter_by(name=username).first()
        if(exist):
            return render_template('registrationResponse.html',response= 'Username already exists please try again with a different username')
        else:
            db.session.add(user)
            db.session.commit()
            return render_template('registrationResponse.html',response= 'User registered successfully')

@app.route('/home/user/<int:iduser>/<int:id>/rate', methods=['GET', 'POST'])
def rate(id,iduser):
    if(request.method == 'POST'):
        rating = request.form['rate']
        song = Song.query.filter_by(id=id).first()
        count = song.count
        rating = (song.rate*count + int(rating))/(count+1)
        count = count + 1
        song.rate = rating
        song.count = count
        db.session.commit()
        songs = Song.query.all()
        return render_template('rate.html',response='Thank you for rating the song ',id = iduser)
@app.route('/home/<int:id>/search', methods=['GET', 'POST'])
def search(id):
    if(request.method == 'POST'):
        tags= request.form['search']
        tag = list(tags.split(','))
        songs = Song.query.all()
        searched = []
        user = User.query.filter_by(id=id).first()
        for song in songs:
            dbtags = list(song.tags.split(','))
            if(set(tag).issubset(dbtags)):
                searched.append(song)
        return render_template('search.html',username=user.name,type ="user",songs=searched)

@app.route('/home/user', methods=['GET', 'POST'])
def user():
    songs = Song.query.all()
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        exist = db.session.query(User.id).filter_by(name=username,password=password).first()
        if(exist):
            return render_template('home.html',username=username,type ="user",songs=songs,id=exist.id)
        else:
            return render_template('loginResponse.html',response= 'Invalid username or password')
@app.route('/home/user/<int:id>', methods=['GET', 'POST'])
def userid(id):
    songs = Song.query.all()
    user = User.query.filter_by(id=id).first()
    return render_template('home.html',username=user.name,type ="user",songs=songs,id=id)

@app.route('/albums', methods=['GET', 'POST'])
def albums():
    albums = Album.query.all()
    Asongs = {}
    for album in albums:
        Asongs[album.name] = []
    for album in albums:
        idsongs = albumSong.query.filter_by(album_id=album.id).all()
        for idsong in idsongs:
            son = Song.query.filter_by(id=idsong.song_id).first()
            Asongs[album.name].append(son)
    return render_template('album.html',albumss=albums,Asongs=Asongs,type='user')

@app.route('/creators/<int:id>', methods=['GET', 'POST'])
def creators(id):
    users = User.query.filter_by(id=id).first()
    creator = Creator.query.all()
    creatorSongs = {}
    for cre in creator:
        creatorSongs[cre.id] = []
        
    for cre in creator:
        songs = Song.query.filter_by(creatorid=cre.id).all()
        creatorSongs[cre.id].append(songs)
    return render_template('creatorSong.html',creators=creator,Csongs=creatorSongs,user=users)
@app.route('/albums/<int:id>', methods=['GET', 'POST'])
def creatorAlbums(id):
    albums = Album.query.filter_by(creatorid=id).all()
    Asongs = {}
    for album in albums:
        Asongs[album.name] = []
    for album in albums:
        idsongs = albumSong.query.filter_by(album_id=album.id).all()
        for idsong in idsongs:
            son = Song.query.filter_by(id=idsong.song_id).first()
            Asongs[album.name].append(son)
    return render_template('album.html',albumss=albums,Asongs=Asongs,type='creator')

@app.route('/playlist/<int:id>', methods=['GET', 'POST'])
def playlistshow(id):
    playlistss = playlist.query.filter_by(userid=id).all()
    Psongs = {}
    for playlists in playlistss:
        Psongs[playlists.name] = []
    for playlists in playlistss:
        idsongs = playlistSong.query.filter_by(playlistid=playlists.id).all()
        for idsong in idsongs:
            son = Song.query.filter_by(id=idsong.songid).first()
            Psongs[playlists.name].append(son)
    return render_template('playlist.html',playlistss=playlistss,Psongs=Psongs,type='user')
@app.route('/playlist/<int:id>/create', methods=['GET', 'POST'])
def createPlaylist(id):
    songs = Song.query.all()
    return render_template('playlistcreation.html',songs=songs,id=id)
@app.route('/playlist/<int:id>/add', methods=['GET', 'POST'])
def addPlaylist(id):
    if(request.method == 'POST'):
        songs = Song.query.all()
        name = request.form['name']
        songid=[]
        for song in songs:
            if(request.form[str(song.id)] == 'add' ):
                songid.append(song.id)
        playlistname = playlist(name=name,userid=id)
        exist = db.session.query(playlist.id).filter_by(name=name).first()
        if(exist):
            return render_template('playlistResponse.html',response= 'Playlist already exists please try again with a different playlist name')
        else:
            db.session.add(playlistname)
            db.session.commit()
            playlistname = playlist.query.filter_by(name=name).first()
            for song in songid:
                playlistsong = playlistSong(playlistid=playlistname.id, songid=song)
                db.session.add(playlistsong)
                db.session.commit()
            return render_template('playlistResponse.html',response= 'Playlist created successfully',id=id)
@app.route('/playlist/<int:id>/delete', methods=['GET', 'POST'])
def playlistdel(id):
    ply = playlist.query.filter_by(id=id).first()
    db.session.query(playlistSong).filter_by(playlistid=id).delete()
    db.session.query(playlist).filter_by(id=id).delete()
    db.session.commit()
    return render_template('playlistResponse.html',response= 'Playlist deleted successfully',id=ply.userid)
@app.route('/playlist/<int:id>/edit', methods=['GET', 'POST'])
def playlistedit(id):
    songs = Song.query.all()
    return render_template('playlistupdate.html',songs=songs,id=id)
@app.route('/playlist/update/<int:id>', methods=['GET', 'POST'])
def playlistupdate(id):
    if(request.method == 'POST'):
        name = request.form['name']
        songs = Song.query.all()
        songid=[]
        for song in songs:
            if(request.form[str(song.id)] == 'add' ):
                songid.append(song.id)
        playlistname = playlist.query.filter_by(id=id).first()
        playlistname.name = name
        db.session.commit()
        db.session.query(playlistSong).filter_by(playlistid=id).delete()
        for song in songid:
            playlistsongs = playlistSong(playlistid=id, songid=song)
            db.session.add(playlistsongs)
            db.session.commit()
        return render_template('playlistResponse.html',response= 'Playlist updated successfully',id=playlistname.userid)
    
@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    user = User.query.filter_by(id=id).first()
    return render_template('profile.html',user=user)