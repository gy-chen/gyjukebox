import requests
import base64
from datetime import timedelta
from datetime import datetime


class BaseClient:
    def search(self, q, offset=0):
        """Search for albums, artists, tracks, playlists

        Args:
            q (str)
            offset (int)

        Returns:
            (albums, artists, tracks, playlists)
        """
        return NotImplemented

    def get_track(self, id_or_uri):
        """Get track information

        Args:
            id_or_uri (str)

        Raises:
            ValueError: if track is not exists

        Returns:
            track information
        """
        return NotImplemented

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
        return NotImplemented

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
        return NotImplemented

    def get_artist_top_tracks(self, id_or_uri):
        """Get artist top tracks

        Args:
            id_or_uri (str)

        Raises:
            ValueError: if artist is not exists

        Returns:
            list of tracks
        """
        return NotImplemented

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
        return NotImplemented


class Client(BaseClient):
    BASE_URL = "https://api.spotify.com"

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = self._exchange_access_token()
        self._expire_time = None

    def _is_expired(self):
        if self._expire_time is None:
            return True
        return self._expire_time <= datetime.now()

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

    def _renew_access_token_if_need(self):
        if self._is_expired():
            self._access_token = self._exchange_access_token()

    def _get_authorization_header(self):
        self._renew_access_token_if_need()
        return f"Bearer {self._access_token}"

    def search(self, q, offset=0):
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
        id = self._extract_id(id_or_uri)
        url = f"{self.BASE_URL}/v1/tracks/{id}"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"market": "TW"}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()

    def get_album_tracks(self, id_or_uri, offset=0):
        id = self._extract_id(id_or_uri)
        url = f"{self.BASE_URL}/v1/albums/{id}/tracks"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"market": "TW", "offset": offset}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]

    def get_artist_albums(self, id_or_uri, offset=0):
        id = self._extract_id(id_or_uri)
        url = f"{self.BASE_URL}/v1/artists/{id}/albums"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"country": "TW", "offset": offset}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]

    def get_artist_top_tracks(self, id_or_uri):
        id = self._extract_id(id_or_uri)
        url = f"{self.BASE_URL}/v1/artists/{id}/top-tracks"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"country": "TW"}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["tracks"]

    def get_playlist_tracks(self, id_or_uri, offset=0):
        id = self._extract_id(id_or_uri)
        url = f"{self.BASE_URL}/v1/playlists/{id}/tracks"
        headers = {"Authorization": self._get_authorization_header()}
        params = {"market": "TW", "offset": offset}
        r = requests.get(url, params=params, headers=headers)
        if not r.ok:
            raise ValueError(r.reason)
        return r.json()["items"]

    def _extract_id(self, id_or_uri):
        componments = id_or_uri.split(":")
        if len(componments) == 3:
            return componments[-1]
        return id_or_uri
