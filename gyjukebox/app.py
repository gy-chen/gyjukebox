from flask import Flask
from gyjukebox.login.web import login_ext
from gyjukebox.oauth.web import oauth_ext
from gyjukebox.spotify.web import spotify_ext
from gyjukebox.login.web.blueprint import bp as login_bp
from gyjukebox.spotify.web.blueprint import bp as spotify_bp


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    login_ext.init_app(app)
    oauth_ext.init_app(app)
    spotify_ext.init_app(app)

    app.register_blueprint(login_bp)
    app.register_blueprint(spotify_bp)

    # TODO start player

    return app