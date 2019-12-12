import os
from gyjukebox.app import create_app


if os.environ.get("FLASK_ENV") == "development":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    app = create_app("config_test")
else:
    app = create_app("config")

