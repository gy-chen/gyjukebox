from flask import Flask
from gyjukebox.login.web import login_ext
from gyjukebox.oauth.web import oauth_ext
from gyjukebox.spotify.web import spotify_ext
from gyjukebox.lyrics.web import lyrics_search_ext
from gyjukebox.login.web.blueprint import bp as login_bp
from gyjukebox.spotify.web.blueprint import bp as spotify_bp
from gyjukebox.lyrics.web.script import lyrics_cli


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    login_ext.init_app(app)
    oauth_ext.init_app(app)
    spotify_ext.init_app(app)
    lyrics_search_ext.init_app(app)

    app.register_blueprint(login_bp)
    app.register_blueprint(spotify_bp)

    app.cli.add_command(lyrics_cli)

    with app.app_context():
        spotify_ext.loop.start()
        spotify_ext.streaming.start()

    return app
