# @name Restaurant Kiosk
# Derived with grudging perminssion from:
# @author: Ash Skabo
# @author: Stuart Skabo
# @year: 2022
# @copyright: BSD 3-Clause licence

import os
import logging as log
import time
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from kiosk.config import Config

# Define the flask app
app = Flask(__name__, static_folder="res")
# setup flask-login module
login = LoginManager(app)
login.login_view = 'login'

# setup flask config
app.config.from_object(Config)

# setup logging
# if not app.debug:
if not os.path.exists('logs'):
    os.mkdir('logs')
log_filename = f"{time.strftime('%Y-%m-%d %H%M%S')}-kiosk.log"
file_handler = RotatingFileHandler(os.path.join('logs',log_filename), maxBytes=20480,
                                    backupCount=10)
file_handler.setFormatter(log.Formatter(
    '%(asctime)-15s %(levelname)-8s: %(message)-s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(log.DEBUG)
app.logger.addHandler(file_handler)

app.logger.setLevel(log.DEBUG)
app.logger.info(f'App name starting:{app.name}')

# setting up sqlalchemy and alembic
app.logger.info("Setting up SQLAlchemy...")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.logger.info("SQLAlchemy initialised")

# setup flask routes
app.logger.info("Importing routes...")
from kiosk import routes, models, errors
app.logger.info("Finished importing routes.py")
