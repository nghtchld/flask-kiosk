import logging as log

from flask import Flask

from kiosk.config import Config
from kiosk.utils import log_debug

log_debug()

log.info("Starting server...")
# Define the flask app
app = Flask(__name__, static_folder="res")

# setup flask config
app.config.from_object(Config)

# setup flask routes
log.info("Importing routes...")
from kiosk import routes
log.info("Finished importing routes.py")

# run main.py database validation and or setup
log.info("Importing and running main.py, DB setup.")
import kiosk.main
log.info("Finished importing main.py")

#Start the flask server
# log.info("Starting server...")
# app.run(port=app.config["port"], host="127.0.0.1")