import os
from dotenv import load_dotenv

load_dotenv("./.env")

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    PORT = os.getenv('PORT', '8080')
    DB = os.getenv('DB', "duck.db")
    SALT = os.getenv('SALT')