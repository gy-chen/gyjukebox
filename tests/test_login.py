from gyjukebox.oauth.web import oauth_ext
from gyjukebox.login.web import login_ext
from gyjukebox.login.web.ext import LoginExt
from gyjukebox.login.web.blueprint import bp as login_bp
from gyjukebox.user.model import User


def test_login(empty_app):
    oauth_ext.init_app(empty_app)
    login_ext.init_app(empty_app)
    empty_app.register_blueprint(login_bp)

    with empty_app.test_client() as client:
        rv = client.get("/login")
        assert rv.status_code == 302


def test_login_jwt(empty_app):
    login_ext.init_app(empty_app)

    user = User("test_sub", "test_name")
    token = login_ext.get_login_jwt_token(user)

    with empty_app.test_request_context(
        "/", headers={"Authorization": f"Bearer {token}"}
    ):
        assert login_ext.get_user_from_request() == user


def test_login_protect(empty_app):
    login_ext.init_app(empty_app)

    @empty_app.route("/")
    @login_ext.required_login
    def _():
        return "Hello"

    user = User("test_sub", "test_name")

    with empty_app.test_client() as client:
        rv = client.get("/")
        assert rv.status_code == 403

        token = login_ext.get_login_jwt_token(user)
        rv = client.get("/", headers={"Authorization": f"Bearer {token}"})
        assert rv.status_code == 200
