from flask import Blueprint
from flask import abort
from flask import request
from flask import jsonify
from gyjukebox.login.web import login_ext
from gyjukebox.spotify.web import spotify_ext
from gyjukebox.spotify.model import RequestTrack, Track
from gyjukebox.lyrics.web import lyrics_search_ext

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
def track_enqueue(id_or_uri):
    try:
        track = spotify_ext.search_client.get_track(id_or_uri)
    except ValueError:
        abort(400)
    track = Track(track["uri"], track["name"], track["artists"], track["duration_ms"])
    user = login_ext.current_user
    request_track = RequestTrack(track, user)
    spotify_ext.next_track_queue.add_track(request_track)
    spotify_ext.player.play()
    return "", 204


@bp.route("/album/<id_or_uri>/enqueue", methods=["POST"])
@login_ext.required_login
def album_enqueue(id_or_uri):
    offset = 0
    tracks = True
    while tracks:
        try:
            tracks = spotify_ext.search_client.get_album_tracks(id_or_uri, offset)
        except ValueError:
            abort(400)
        for track in tracks:
            track = Track(
                track["uri"], track["name"], track["artists"], track["duration_ms"]
            )
            user = login_ext.current_user
            request_track = RequestTrack(track, user)
            spotify_ext.next_track_queue.add_track(request_track)
        # spotify default album tracks limit
        offset += 20
    spotify_ext.player.play()
    return "", 204


@bp.route("/playlist/<id_or_uri>/enqueue", methods=["POST"])
@login_ext.required_login
def playlist_enqueue(id_or_uri):
    offset = 0
    playlist_tracks = True
    while playlist_tracks:
        try:
            playlist_tracks = spotify_ext.search_client.get_playlist_tracks(
                id_or_uri, offset
            )
        except ValueError:
            abort(400)
        for playlist_track in playlist_tracks:
            track = playlist_track["track"]
            track = Track(
                track["uri"], track["name"], track["artists"], track["duration_ms"]
            )
            user = login_ext.current_user
            request_track = RequestTrack(track, user)
            spotify_ext.next_track_queue.add_track(request_track)
        # spotify default playlist tracks limit
        offset += 100
    spotify_ext.player.play()
    return "", 204


@bp.route("/track/current")
@login_ext.required_login
def get_current_track():
    current_request_track = spotify_ext.player.get_playing_track()
    if current_request_track is None:
        return jsonify(track=None, user=None)
    track = {
        "uri": current_request_track.track.uri,
        "name": current_request_track.track.name,
        "artists": current_request_track.track.artists,
        "duration_ms": current_request_track.track.duration_ms,
    }
    user = {"name": current_request_track.user.name}
    return jsonify(track=track, user=user)


@bp.route("/lyrics/current")
@login_ext.required_login
def get_current_track_lyrics():
    current_request_track = spotify_ext.player.get_playing_track()
    if current_request_track is None:
        return jsonify(lyrics=None)
    lyrics = None
    searched_lyrics = lyrics_search_ext.searcher.search(
        " ".join(artist["name"] for artist in current_request_track.track.artists),
        current_request_track.track.name,
    )
    if searched_lyrics:
        lyrics = {
            "artist": searched_lyrics.artist,
            "title": searched_lyrics.title,
            "lyrics": searched_lyrics.lyrics,
        }
    return jsonify(lyrics=lyrics)


@bp.route("/album/<id_or_uri>/tracks")
@login_ext.required_login
def get_album_tracks(id_or_uri):
    offset = request.args.get("offset", 0)
    try:
        tracks = spotify_ext.search_client.get_album_tracks(id_or_uri, offset)
    except ValueError:
        abort(400)
    return jsonify(tracks=tracks)


@bp.route("/artist/<id_or_uri>/details")
@login_ext.required_login
def get_artist_details(id_or_uri):
    offset = request.args.get("offset", 0)
    try:
        tracks = spotify_ext.search_client.get_artist_top_tracks(id_or_uri)
        albums = spotify_ext.search_client.get_artist_albums(id_or_uri, offset)
    except ValueError:
        abort(400)
    return jsonify(tracks=tracks, albums=albums)


@bp.route("/playlist/<id_or_uri>/tracks")
@login_ext.required_login
def get_playlist_tracks(id_or_uri):
    offset = request.args.get("offset", 0)
    try:
        tracks = spotify_ext.search_client.get_playlist_tracks(id_or_uri, offset)
    except ValueError:
        abort(400)
    return jsonify(tracks=tracks)


@bp.route("/me/top")
@login_ext.required_login
def get_user_top():
    offset = request.args.get("offset", 0)
    try:
        top_artists = spotify_ext.search_client.get_user_top_artists(offset)
        top_tracks = spotify_ext.search_client.get_user_top_tracks(offset)
    except ValueError:
        abort(400)
    return jsonify(artists=top_artists, tracks=top_tracks)


@bp.route("/me/playlists")
@login_ext.required_login
def get_user_playlists():
    offset = request.args.get("offset", 0)
    try:
        user_playlists = spotify_ext.search_client.get_user_playlists(offset)
    except ValueError:
        abort(400)
    return jsonify(playlists=user_playlists)


@bp.route("/me/albums")
@login_ext.required_login
def get_user_albums():
    offset = request.args.get("offset", 0)
    try:
        user_albums = spotify_ext.search_client.get_user_albums(offset)
    except ValueError:
        abort(400)
    return jsonify(albums=user_albums)


@bp.route("/me/artists")
@login_ext.required_login
def get_user_artists():
    after = request.args.get("after", None)
    try:
        user_artists = spotify_ext.search_client.get_user_artists(after)
    except ValueError:
        abort(400)
    return jsonify(artists=user_artists)


@bp.route("/me/tracks")
@login_ext.required_login
def get_user_tracks():
    offset = request.args.get("offset", 0)
    try:
        user_tracks = spotify_ext.search_client.get_user_tracks(offset)
    except ValueError:
        abort(400)
    return jsonify(tracks=user_tracks)
