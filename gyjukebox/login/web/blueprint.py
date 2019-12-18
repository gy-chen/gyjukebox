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


@bp.route("/login")
def login():
    google_provider = oauth_ext.google_provider
    authorization_url = google_provider.get_authorization_url()
    callback_url = request.args.get("callback_url")
    if login_ext.is_valid_callback_url(callback_url):
        session["login_callback_url"] = callback_url
    return redirect(authorization_url)


@bp.route("/login/callback")
def login_callback():
    google_provider = oauth_ext.google_provider
    oauth_user = google_provider.fetch_user()
    user = User(oauth_user["sub"], oauth_user["name"])
    token = login_ext.get_login_jwt_token(user)

    callback_url = session.get("login_callback_url")
    if callback_url is not None:
        return redirect(Href(callback_url)(token=token))
    return jsonify(token=token)
