import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv("./.env")

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    PORT = os.getenv('PORT', '8080')
    DB = os.getenv('DB', "duck.db")
    SALT = os.getenv('SALT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, os.environ.get('DATABASE'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False