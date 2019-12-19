from flask import Blueprint
from flask import redirect
from flask import jsonify
from flask import request
from flask import session
from werkzeug.urls import Href
from gyjukebox.login.web import login_ext
from gyjukebox.oauth.web import oauth_ext
from gyjukebox.user.model import User

bp = Blueprint("login", __name__)


@bp.route("/login/google")
def google_login():
    google_provider = oauth_ext.google_provider
    authorization_url = google_provider.get_authorization_url()
    return _login(authorization_url)


@bp.route("/login/google/callback")
def google_login_callback():
    google_provider = oauth_ext.google_provider
    token = google_provider.fetch_token(request.url)
    oauth_user = google_provider.fetch_user(token)
    user = User(oauth_user["sub"], oauth_user["name"])
    return _login_callback(user, token)


@bp.route("/login/spotify")
def spotify_login():
    spotify_provider = oauth_ext.spotify_provider
    authorization_url = spotify_provider.get_authorization_url()
    return _login(authorization_url)


@bp.route("/login/spotify/callback")
def spotify_login_callback():
    spotify_provider = oauth_ext.spotify_provider
    token = spotify_provider.fetch_token(request.url)
    oauth_user = spotify_provider.fetch_user(token)
    user = User(oauth_user["uri"], oauth_user["display_name"])
    return _login_callback(user, token)


def _login(authorization_url):
    callback_url = request.args.get("callback_url")
    if login_ext.is_valid_callback_url(callback_url):
        session["login_callback_url"] = callback_url
    return redirect(authorization_url)


def _login_callback(user, token):
    token_saver = oauth_ext.get_token_saver(user)
    token_saver.save(token)

    jwt_token = login_ext.get_login_jwt_token(user)
    callback_url = session.get("login_callback_url")
    if callback_url is not None:
        return redirect(Href(callback_url)(token=jwt_token))
    return jsonify(token=jwt_token)
