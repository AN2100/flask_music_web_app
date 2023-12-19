import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    Debug = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = None

class LocalDevelopmentConfig(Config):
    Debug = True
    SQLITE_DB_DIR = os.path.join(basedir, '../db_directory')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'databaseMusic')