import os
import logging
from gyjukebox.app import create_app


if os.environ.get("FLASK_ENV") == "development":
    logging.basicConfig(level=logging.DEBUG)
    app = create_app("config_test")
else:
    logging.basicConfig(level=logging.INFO)
    app = create_app("config")

