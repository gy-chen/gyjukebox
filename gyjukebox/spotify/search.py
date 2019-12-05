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
        r.raise_for_status()
        j_data = r.json()
        albums, artists, tracks, playlists = (
            j_data["albums"]["items"],
            j_data["artists"]["items"],
            j_data["tracks"]["items"],
            j_data["playlists"]["items"],
        )
        return albums, artists, tracks, playlists
