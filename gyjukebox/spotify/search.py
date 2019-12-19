import requests
import base64
from datetime import timedelta
from datetime import datetime


class BaseClient:
    BASE_URL = "https://api.spotify.com"

    def __init__(self):
        self._access_token = None
        self._expire_time = None

    def _is_expired(self):
        """Is token expired?

        Returns:
            boolean
        """
        if self._expire_time is None:
            return True
        return self._expire_time <= datetime.now()

    def _exchange_access_token(self):
        """Exchange or renew access token

        Returns:
            new access token string
        """
        return NotImplemented

    def _renew_access_token_if_need(self):
        if self._is_expired():
            self._access_token = self._exchange_access_token()

    def _get_authorization_header(self):
        self._renew_access_token_if_need()
        return f"Bearer {self._access_token}"

    def _extract_id(self, id_or_uri):
        componments = id_or_uri.split(":")
        if len(componments) == 3:
            return componments[-1]
        return id_or_uri

    def search(self, q, offset=0):
        """Search for albums, artists, tracks, playlists

        Args:
            q (str)
            offset (int)

        Returns:
            (albums, artists, tracks, playlists)
        """
        url = f"{self.BASE_URL}/v1/search"
        headers = {"Authorization": self._get_authorization_header()}
        params = {
            "q": q,
            "type": "album,artist,playlist,track",
            "market": "TW",
            "offset": offset,
        }
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        j_data = r.json()
        albums, artists, tracks, playlists = (
            j_data["albums"]["items"],
            j_data["artists"]["items"],
            j_data["tracks"]["items"],
            j_data["playlists"]["items"],
        )
        return albums, artists, tracks, playlists

    def get_track(self, id_or_uri):
        """Get track information

        Args:
            id_or_uri (str)

        Raises:
            ValueError: if track is not exists

        Returns:
            track information
        """
        id = self._extract_id(id_or_uri)
        url = f"{self.BASE_URL}/v1/tracks/{id}"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"market": "TW"}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()

    def get_album_tracks(self, id_or_uri, offset=0):
        """Get album tracks

        Args:
            id_or_uri (str)
            offset (int)

        Raises:
            ValueError: if album is not exists

        Returns:
            list of tracks
        """
        id = self._extract_id(id_or_uri)
        url = f"{self.BASE_URL}/v1/albums/{id}/tracks"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"market": "TW", "offset": offset}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]

    def get_artist_albums(self, id_or_uri, offset=0):
        """Get artist albums

        Args:
            id_or_uri (str)
            offset (int)
        
        Raises:
            ValueError: if artist is not exists

        Returns:
            list of albums
        """
        id = self._extract_id(id_or_uri)
        url = f"{self.BASE_URL}/v1/artists/{id}/albums"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"country": "TW", "offset": offset}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]

    def get_artist_top_tracks(self, id_or_uri):
        """Get artist top tracks

        Args:
            id_or_uri (str)

        Raises:
            ValueError: if artist is not exists

        Returns:
            list of tracks
        """
        id = self._extract_id(id_or_uri)
        url = f"{self.BASE_URL}/v1/artists/{id}/top-tracks"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"country": "TW"}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["tracks"]

    def get_playlist_tracks(self, id_or_uri, offset=0):
        """Get playlist tracks

        Args:
            id_or_uri (str)
            offset (int)

        Raises:
            ValueError: if playlist is not exists

        Returns:
            list of tracks
        """
        id = self._extract_id(id_or_uri)
        url = f"{self.BASE_URL}/v1/playlists/{id}/tracks"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"market": "TW", "offset": offset}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]

    def get_user_top_artists(self, offset=0):
        """Get user's top artists

        Args:
            offset (int)

        Returns:
            list of artists
        """
        return NotImplemented

    def get_user_top_tracks(self, offset=0):
        """Get user's top tracks

        Args:
            offset (int)

        Returns:
            list of tracks
        """
        return NotImplemented

    def get_user_playlists(self, offset=0):
        """Get user's saved playlists

        Args:
            offset (int)

        Returns:
            list of playlists
        """
        return NotImplemented

    def get_user_albums(self, offset=0):
        """Get user's saved albums

        Args:
            offset (int)

        Returns:
            list of albums
        """
        return NotImplemented

    def get_user_artists(self, after=None):
        """Get user's saved artists

        Args:
            after (str): The last artist ID retrieved from the previous request.

        Returns:
            list of artists
        """
        return NotImplemented

    def get_user_tracks(self, offset=0):
        """Get user's saved tracks

        Args:
            offset (int)

        Returns:
            list of tracks
        """
        return NotImplemented


class Client(BaseClient):
    BASE_URL = "https://api.spotify.com"

    def __init__(self, client_id, client_secret):
        super().__init__()
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = self._exchange_access_token()

    def _encode_client_info(self, client_id, client_secret):
        content = f"{client_id}:{client_secret}"
        return base64.b64encode(content.encode()).decode()

    def _exchange_access_token(self):
        headers = {
            "Authorization": f"Basic {self._encode_client_info(self._client_id, self._client_secret)}"
        }
        data = {"grant_type": "client_credentials"}
        r = requests.post(
            "https://accounts.spotify.com/api/token", data=data, headers=headers
        )
        r.raise_for_status()
        data = r.json()
        self._expire_time = datetime.now() + timedelta(seconds=data["expires_in"])
        return data["access_token"]

    def get_user_top_artists(self, offset=0):
        return None

    def get_user_top_tracks(self, offset=0):
        return None

    def get_user_playlists(self, offset=0):
        return None

    def get_user_albums(self, offset=0):
        return None

    def get_user_artists(self, after=None):
        return None

    def get_user_tracks(self, offset=0):
        return None


class OAuthClient(BaseClient):
    """Use Spotify OAuth to obtain extra data like user's tracks, albums, etc.

    Args:
        provider (gyjukebox.oauth.provider.SpotifyOAuthProvider)
        token_saver (gyjukebox.oauth.token_saver.TokenSaver)
    """

    BASE_URL = "https://api.spotify.com"

    def __init__(self, provider, token_saver):
        super().__init__()
        self._provider = provider
        self._token_saver = token_saver
        token = self._token_saver.get()
        if token is not None:
            self._access_token = token["access_token"]
            self._expire_time = datetime.fromtimestamp(token["expires_at"])

    def _exchange_access_token(self):
        """Exchange or renew access token

        Returns:
            new access token string
        """
        token = self._token_saver.get()
        new_token = self._provider.refresh_token(token)
        self._expire_time = datetime.fromtimestamp(new_token["expires_at"])
        self._token_saver.save(new_token)
        return new_token["access_token"]

    def get_user_top_artists(self, offset=0):
        url = f"{self.BASE_URL}/v1/me/top/artists"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"offset": offset}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]

    def get_user_top_tracks(self, offset=0):
        url = f"{self.BASE_URL}/v1/me/top/tracks"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"offset": offset}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]

    def get_user_playlists(self, offset=0):
        url = f"{self.BASE_URL}/v1/me/playlists"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"offset": offset}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]

    def get_user_albums(self, offset=0):
        url = f"{self.BASE_URL}/v1/me/albums"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"offset": offset, "market": "TW"}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]

    def get_user_artists(self, after=None):
        url = f"{self.BASE_URL}/v1/me/following"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"type": "artist", "after": after}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]

    def get_user_tracks(self, offset=0):
        url = f"{self.BASE_URL}/v1/me/tracks"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"offset": offset, "market": "TW"}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]
