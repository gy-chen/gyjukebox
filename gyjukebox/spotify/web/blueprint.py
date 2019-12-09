from flask import Blueprint
from flask import abort
from flask import request
from flask import jsonify
from gyjukebox.login.web import login_ext
from gyjukebox.spotify.web import spotify_ext
from gyjukebox.spotify.model import RequestTrack

bp = Blueprint("spotify", __name__)


@bp.route("/search")
@login_ext.required_login
def search():
    q = request.args.get("q")
    offset = request.args.get("offset", 0)
    if not q:
        abort(400)
    try:
        offset = int(offset)
        albums, artists, tracks, playlists = spotify_ext.search_client.search(q, offset)
    except ValueError:
        abort(400)
    return jsonify(albums=albums, artists=artists, tracks=tracks, playlists=playlists)


@bp.route("/track/<id_or_uri>/enqueue", methods=["POST"])
@login_ext.required_login
def enqueue(id_or_uri):
    try:
        track = spotify_ext.search_client.get_track(id_or_uri)
    except ValueError:
        abort(400)
    user = login_ext.current_user
    request_track = RequestTrack(track, user)
    spotify_ext.next_track_queue.add_track(request_track)
    return "", 204


@bp.route("/track/current")
@login_ext.required_login
def get_current_track():
    current_request_track = spotify_ext.player.get_playing_track()
    return jsonify(current_request_track)


@bp.route("/album/<id_or_uri>/tracks")
@login_ext.required_login
def get_album_tracks(id_or_uri):
    try:
        tracks = spotify_ext.search_client.get_album_tracks(id_or_uri)
    except ValueError:
        abort(400)
    return jsonify(tracks=tracks)
