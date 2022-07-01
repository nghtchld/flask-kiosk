import logging as log

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from kiosk.config import Config
from kiosk.utils import log_debug

log_debug()

log.info("Starting server...")
# Define the flask app
app = Flask(__name__, static_folder="res")
# setup flask-login module
login = LoginManager(app)
login.login_view = 'login'

# setup flask config
app.config.from_object(Config)

# setting up sqlalchemy and alembic
log.info("Setting up SQLAlchemy...")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
log.info("SQLAlchemy initialised")

# setup flask routes
log.info("Importing routes...")
from kiosk import routes, models
log.info("Finished importing routes.py")

# run main.py database validation and or setup
log.info("Importing main.py init logging and check DB setup.")
import kiosk.main
log.info("Finished importing main.py")