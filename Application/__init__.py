from flask import Flask
from flask import render_template
from flask import request
from flask import current_app as app
from Application.models import User, Creator, Admin, Song, Album, albumSong ,playlist,playlistSong
from Application.database import db
import os
curr_dir = os.path.abspath(os.path.dirname(__file__))