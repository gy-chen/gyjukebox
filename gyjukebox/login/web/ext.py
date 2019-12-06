import functools
import jwt
from flask import abort
from flask import current_app
from flask import request
from flask import g
from gyjukebox.user.model import User


class LoginExt:
    def __init__(self, app=None):
        self._app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("LOGIN_JWT_SECRET", None)
        app.config.setdefault("LOGIN_VALID_CALLBACK_URLS", [])

    @property
    def app(self):
        return self._app or current_app

    def get_login_jwt_token(self, user):
        """Generate token for login user

        Args:
            user (gyjukebox.user.model.User)

        Returns:
            jwt token string
        """
        secret = self.app.config["LOGIN_JWT_SECRET"]
        token = jwt.encode(
            {"sub": user.sub, "name": user.name}, secret, algorithm="HS256"
        )
        return token.decode()

    def get_user_from_request(self):
        token = self._get_token_from_request()
        if token is None:
            return None
        try:
            user_dict = jwt.decode(
                token, self.app.config["LOGIN_JWT_SECRET"], algorithms=["HS256"]
            )
            return User(user_dict["sub"], user_dict["name"])
        except jwt.InvalidTokenError as e:
            current_app.logger.info("failed to login: %s", e)
            return None

    def _get_token_from_request(self):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header:
            return None
        try:
            _, token = auth_header.split()
            return token
        except ValueError:
            return None

    @property
    def current_user(self):
        if "login_current_user" not in g:
            g.current_user = self.get_user_from_request()
        return g.current_user

    def required_login(self, f):
        @functools.wraps(f)
        def wrapper(*args, **kargs):
            if self.current_user is None:
                abort(403)
            return f(*args, **kargs)

        return wrapper

    def is_valid_callback_url(self, callback_url):
        return any(
            callback_url.startswith(valid_url)
            for valid_url in self.app.config["LOGIN_VALID_CALLBACK_URLS"]
        )
