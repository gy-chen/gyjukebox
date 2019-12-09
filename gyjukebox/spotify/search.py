import requests
import base64


class Client:
    BASE_URL = "https://api.spotify.com"

    def __init__(self, client_id, client_secret):
        self._access_token = self._exchange_access_token(client_id, client_secret)

    def _encode_client_info(self, client_id, client_secret):
        content = f"{client_id}:{client_secret}"
        return base64.b64encode(content.encode()).decode()

    def _exchange_access_token(self, client_id, client_secret):
        headers = {
            "Authorization": f"Basic {self._encode_client_info(client_id, client_secret)}"
        }
        data = {"grant_type": "client_credentials"}
        r = requests.post(
            "https://accounts.spotify.com/api/token", data=data, headers=headers
        )
        r.raise_for_status()
        # TODO need to deal with expires?
        return r.json()["access_token"]

    def _get_authorization_header(self):
        return f"Bearer {self._access_token}"

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

    def _extract_id(self, id_or_uri):
        componments = id_or_uri.split(":")
        if len(componments) == 3:
            return componments[-1]
        return id_or_uri
