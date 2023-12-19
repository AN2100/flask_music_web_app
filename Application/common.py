from Application import *
@app.route('/aboutus')
def aboutus():
    return render_template('about.html')
@app.route('/')
def homePage():
    return render_template('index.html')