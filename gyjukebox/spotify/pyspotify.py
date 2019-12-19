import threading
import pathlib
import spotify


def create_logged_in_session(username, password):
    """Create pyspotify session and wait user logged in

    Args:
        username (str)
        password (str)

    Returns:
        spotify.Session instance
    """
    spotify_config = spotify.Config()
    spotify_config.load_application_key_file(
        pathlib.Path(__file__).parent / "spotify_appkey.key"
    )

    session = spotify.Session(spotify_config)
    loop = spotify.EventLoop(session)

    logged_in = threading.Event()

    def on_connection_state_updated(session):
        if session.connection.state is spotify.ConnectionState.LOGGED_IN:
            logged_in.set()

    session.on(
        spotify.SessionEvent.CONNECTION_STATE_UPDATED, on_connection_state_updated
    )

    loop.start()
    session.login(username, password)
    logged_in.wait()
    loop.stop()

    return session
