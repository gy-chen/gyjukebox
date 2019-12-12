import threading
import logging
import gi
import spotify
from time import time

gi.require_version("Gst", "1.0")
from gi.repository import GObject, Gst

logger = logging.getLogger(__name__)


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
        self._timestamp = None
        self._timestamp_lock = threading.RLock()
        self._session.on(
            spotify.SessionEvent.MUSIC_DELIVERY,
            self._on_music_delivery_callback,
            self._playing,
            self._appsrc,
        )
        self._session.on(spotify.SessionEvent.END_OF_TRACK, self._on_end_of_track)

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

        if hlssink2_options.get("location"):
            sink.set_property("location", hlssink2_options.get("location"))

        if hlssink2_options.get("playlist-root"):
            sink.set_property("playlist-root", hlssink2_options.get("playlist-root"))

        if hlssink2_options.get("playlist-location"):
            sink.set_property(
                "playlist-location", hlssink2_options.get("playlist-location")
            )

        if hlssink2_options.get("target-duration"):
            sink.set_property(
                "target-duration", int(hlssink2_options.get("target-duration"))
            )

        if hlssink2_options.get("max-files"):
            sink.set_property("max-files", int(hlssink2_options.get("max-files")))

        if hlssink2_options.get("playlist-length"):
            sink.set_property(
                "playlist-length", int(hlssink2_options.get("playlist-length"))
            )

        # TODO add other hlssink2 options

        pipeline.add(appsrc, audioconvert, voaacenc, sink)

        appsrc.link(audioconvert)
        audioconvert.link(voaacenc)
        voaacenc.link(sink)

        return pipeline, appsrc

    def _on_end_of_track(self, _):
        logger.info("end of track, reset timestamp")
        with self._timestamp_lock:
            self._timestamp = None

    def _is_music_delivery_too_fast(self, duration):
        with self._timestamp_lock:
            return self._timestamp + duration > time() * Gst.SECOND

    def _on_music_delivery_callback(
        self, session, audio_format, frames, num_frames, playing, appsrc
    ):
        with self._timestamp_lock:
            if self._timestamp is None:
                logger.info("no timestamp, set to current time")
                self._timestamp = time() * Gst.SECOND
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
        if self._is_music_delivery_too_fast(duration):
            logger.info("music delivery too fast")
            return 0
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
    import config
    import logging
    from gyjukebox.spotify.pyspotify import create_logged_in_session

    logging.basicConfig(level=logging.DEBUG)

    Gst.init(sys.argv)

    track_uri = "spotify:track:6xZtSE6xaBxmRozKA0F6TA"
    end_of_track = threading.Event()
    session = create_logged_in_session(config.SPOTIFY_USERNAME, config.SPOTIFY_PASSWORD)
    s = SpotifyStreaming(session)
    loop = spotify.EventLoop(session)

    def on_end_of_track(self):
        end_of_track.set()

    session.on(spotify.SessionEvent.END_OF_TRACK, on_end_of_track)

    loop.start()
    track = session.get_track(track_uri).load()
    session.player.load(track)
    session.player.play()
    s.start()
    end_of_track.wait()
