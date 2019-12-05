import threading
import gi
import spotify

gi.require_version("Gst", "1.0")
from gi.repository import GObject, Gst


class SpotifyStreaming:
    """Spotify streaming using hls

    GStreamer pipeline:
        1. appsrc
        2. audioconvert
        3. voaacenc
        4. hlssink2

    Args:
        session (spotify.Session)
        hlssink2_options (dict)
    """

    GST_CAPS = "audio/x-raw,format=S16LE,rate=44100,channels=2,layout=interleaved"

    def __init__(self, session, hlssink2_options={}):
        self._session = session
        self._pipeline, self._appsrc = self._create_pipeline(hlssink2_options)
        self._playing = threading.Event()
        self._timestamp = 0
        self._timestamp_lock = threading.RLock()
        self._session.on(
            spotify.SessionEvent.MUSIC_DELIVERY,
            self._on_music_delivery_callback,
            self._playing,
            self._appsrc,
        )

    def start(self):
        self._playing.set()
        self._pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        self._pipeline.set_state(Gst.State.NULL)
        self._playing.clear()

    def _create_pipeline(self, hlssink2_options):
        pipeline = Gst.Pipeline()

        appsrc = Gst.ElementFactory.make("appsrc")
        appsrc.set_property("caps", Gst.Caps.from_string(self.GST_CAPS))
        appsrc.set_property("format", "time")

        audioconvert = Gst.ElementFactory.make("audioconvert")

        voaacenc = Gst.ElementFactory.make("voaacenc")

        sink = Gst.ElementFactory.make("hlssink2")

        if hlssink2_options.get("playlist-root"):
            sink.set_property("playlist-root", hlssink2_options.get("playlist-root"))

        if hlssink2_options.get("playlist-location"):
            sink.set_property(
                "playlist-location", hlssink2_options.get("playlist-location")
            )

        # TODO add other hlssink2 options

        pipeline.add(appsrc, audioconvert, voaacenc, sink)

        appsrc.link(audioconvert)
        audioconvert.link(voaacenc)
        voaacenc.link(sink)

        return pipeline, appsrc

    def _on_music_delivery_callback(
        self, session, audio_format, frames, num_frames, playing, appsrc
    ):
        if not playing.is_set():
            return 0
        if not frames:
            return 0

        # copied from mopidy spotify
        known_format = (
            audio_format.sample_type == spotify.SampleType.INT16_NATIVE_ENDIAN
        )
        assert known_format, "Expects 16-bit signed integer samples"

        # https://gstreamer.freedesktop.org/documentation/tutorials/basic/short-cutting-the-pipeline.htm
        duration = Gst.util_uint64_scale(
            num_frames, Gst.SECOND, audio_format.sample_rate
        )
        buffer = Gst.Buffer.new_wrapped(bytes(frames))
        with self._timestamp_lock:
            buffer.pts = self._timestamp
            buffer.duration = duration
            self._timestamp += duration

        if appsrc.emit("push-buffer", buffer) == Gst.FlowReturn.OK:
            return num_frames
        return 0


if __name__ == "__main__":
    import sys
    import pathlib
    import config
    import logging
    logging.basicConfig(level=logging.DEBUG)

    Gst.init(sys.argv)

    track_uri = 'spotify:track:6xZtSE6xaBxmRozKA0F6TA'
    logged_in = threading.Event()
    end_of_track = threading.Event()
    spotify_config = spotify.Config()
    spotify_config.load_application_key_file(
        pathlib.Path(__file__).parent / "spotify_appkey.key"
    )
    session = spotify.Session(spotify_config)
    s = SpotifyStreaming(session)
    loop = spotify.EventLoop(session)

    def on_connection_state_updated(session):
        if session.connection.state is spotify.ConnectionState.LOGGED_IN:
            logged_in.set()

    def on_end_of_track(self):
        end_of_track.set()

    session.on(
        spotify.SessionEvent.CONNECTION_STATE_UPDATED, on_connection_state_updated
    )
    session.on(spotify.SessionEvent.END_OF_TRACK, on_end_of_track)

    loop.start()
    session.login(config.SPOTIFY_USERNAME, config.SPOTIFY_PASSWORD)

    logged_in.wait()
    track = session.get_track(track_uri).load()
    session.player.load(track)
    session.player.play()
    s.start()
    end_of_track.wait()
