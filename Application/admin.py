from Application import *
import matplotlib.pyplot as plt
from multiprocessing import Process
import numpy as np
def plot_graph(keys, values):
    plt.bar(keys, values, color='g')
    plt.xlabel('Songs')
    plt.ylabel('Count')
    plt.title('Song Count')
    plt.savefig('static/songcount.png')

@app.route('/login/admin', methods=['GET', 'POST'])
def adminLogin():
    return render_template('login.html',form_type = 'Admin login')
@app.route('/home/admin', methods=['GET', 'POST'])
def admin():
    songs = Song.query.all()
    if(request.method == 'POST'):
        gmdflkgnklgnbgkdfngklndfkgdfklgnkdflg
        
        username = request.form['username']
        password = request.form['password']
        exist = db.session.query(Admin.id).filter_by(name=username,password=password).first()
        if(exist):
            return render_template('home.html',username=username,type ="Admin",songs=songs)
        else:
            return render_template('loginResponse.html',response= 'Invalid username or password')
    if(request.method == 'GET'):
        return render_template('home.html',username='admin',type ="Admin",songs=songs)
@app.route('/home/admin/controls', methods=['GET', 'POST'])
def admincontrols():
    users = User.query.all()
    creators = Creator.query.all()
    songs = Song.query.all()
    son = {}
    for i in songs:
        son[i.name] = i.count
    p = Process(target=plot_graph, args=(son.keys(), son.values()))
    p.start()
    p.join()

    
    return render_template('admin.html',users=users,creators=creators,songs=songs)

@app.route('/user/<int:id>/delete', methods=['GET', 'POST'])
def deleteuser(id):
    songs = Song.query.all()
    pl = playlist.query.filter_by(userid=id).all()
    for p in pl:
        db.session.query(playlistSong).filter_by(playlistid=p.id).delete()
    db.session.query(playlist).filter_by(userid=id).delete()
    db.session.query(User).filter_by(id=id).delete()
    db.session.commit()
    users = User.query.all()
    creators = Creator.query.all()
    songs = Song.query.all()
    return render_template('admin.html',users=users,creators=creators,songs=songs)
@app.route('/creator/<int:id>/delete', methods=['GET', 'POST'])
def deletecreator(id):
    songs = Song.query.all()
    al = Album.query.filter_by(creatorid=id).all()
    for a in al:
        db.session.query(albumSong).filter_by(album_id=a.id).delete()
    db.session.query(Album).filter_by(creatorid=id).delete()
    db.session.query(Creator).filter_by(id=id).delete()
    db.session.commit()
    users = User.query.all()
    creators = Creator.query.all()
    songs = Song.query.all()
    return render_template('admin.html',users=users,creators=creators,songs=songs)
@app.route('/creator/<int:id>/Blacklist', methods=['GET', 'POST'])
def blacklistcreator(id):
    songs = Song.query.all()
    al = Album.query.filter_by(creatorid=id).all()
    cre= Creator.query.filter_by(id=id).first()
    cre.allow = 0
    db.session.commit()
    users = User.query.all()
    creators = Creator.query.all()
    songs = Song.query.all()
    return render_template('admin.html',users=users,creators=creators,songs=songs)
@app.route('/creator/<int:id>/Allow', methods=['GET', 'POST'])
def allowcreator(id):
    songs = Song.query.all()
    al = Album.query.filter_by(creatorid=id).all()
    cre= Creator.query.filter_by(id=id).first()
    cre.allow = 1
    db.session.commit()
    users = User.query.all()
    creators = Creator.query.all()
    songs = Song.query.all()
    return render_template('admin.html',users=users,creators=creators,songs=songs)
@app.route('/song/<int:id>/delete', methods=['GET', 'POST'])
def deletesong(id):
    songs = Song.query.all()
    # songdel = Song.query.filter_by(id=id).first()
    # os.remove(os.path.join(curr_dir, 'static', songdel.path))
    # os.remove(os.path.join(curr_dir, 'static', songdel.image))
    db.session.query(albumSong).filter_by(song_id=id).delete()
    db.session.query(Song).filter_by(id=id).delete()
    db.session.commit()
    users = User.query.all()
    creators = Creator.query.all()
    songs = Song.query.all()
    return render_template('admin.html',users=users,creators=creators,songs=songs)