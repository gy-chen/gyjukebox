from gyjukebox.login.web import login_ext
from gyjukebox.spotify.web import spotify_ext
from gyjukebox.spotify.web.blueprint import bp


def test_non_login(empty_app):
    login_ext.init_app(empty_app)
    spotify_ext.init_app(empty_app)
    empty_app.register_blueprint(bp)

    with empty_app.test_client() as client:
        rv = client.get("/search")
        assert rv.status_code == 403

        rv = client.post("/track/spotify:track:6xZtSE6xaBxmRozKA0F6TA/enqueue")
        assert rv.status_code == 403

        rv = client.get("/track/current")
        assert rv.status_code == 403

        rv = client.get("/album/spotify:album:7jyiXKzJYgJ24IqlGMKcjN/tracks")
        assert rv.status_code == 403


def test_without_error(empty_app, login_token):
    login_ext.init_app(empty_app)
    spotify_ext.init_app(empty_app)
    empty_app.register_blueprint(bp)

    headers = {"Authorization": f"Bearer {login_token}"}

    with empty_app.test_client() as client:
        rv = client.get("/search?q=Hello", headers=headers)
        assert rv.status_code == 200

        rv = client.post(
            "/track/spotify:track:6xZtSE6xaBxmRozKA0F6TA/enqueue", headers=headers
        )
        assert rv.status_code == 204

        rv = client.get("track/current", headers=headers)
        assert rv.status_code == 200

        rv = client.get("/album/spotify:album:7jyiXKzJYgJ24IqlGMKcjN/tracks", headers=headers)
        assert rv.status_code == 200
        