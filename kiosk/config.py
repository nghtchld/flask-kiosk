import os
from dotenv import load_dotenv
import logging as log

from kiosk.utils import log_debug
log_debug()

basedir = os.path.abspath(os.path.dirname(__file__))
log.debug(f"basedir set as {basedir}")

log.debug("loading ./.env variables to Config.")
load_dotenv("./.env")

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-will-never-guess'
    PORT = os.getenv('PORT', '8080')
    SALT = os.getenv('SALT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, os.environ.get('DATABASE'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False