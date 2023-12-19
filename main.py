import os
from flask import Flask
from Application import config
from Application.database import db
from Application.config import LocalDevelopmentConfig
app = None

def create_app():
    app = Flask(__name__,template_folder='templates')
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    app.logger.info('Creating app...')
    return app

app = create_app()
from Application.controllers import *

if __name__ == '__main__':
    app.run(debug=True,port=5568)