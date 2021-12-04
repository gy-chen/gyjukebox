import threading
import logging
import gi
from time import time

gi.require_version("Gst", "1.0")
from gi.repository import GObject, Gst

logger = logging.getLogger(__name__)


class HLSStreaming:
    GST_CAPS = "audio/x-raw,format=S16LE,rate=44100,channels=2,layout=interleaved"

    def __init__(self, hlssink2_options={}):
        self._pipeline, self._appsrc = self._create_pipeline(hlssink2_options)
        self._playing = threading.Event()
        self._timestamp = None
        self._timestamp_lock = threading.RLock()

    def start(self):
        self._playing.set()
        self._pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        self._pipeline.set_state(Gst.State.NULL)
        self._playing.clear()

    def on_end_of_track(self):
        logger.debug("end of track, reset timestamp")
        with self._timestamp_lock:
            self._timestamp = None

    def on_music_delivery(self, frames, num_frames):
        with self._timestamp_lock:
            if self._timestamp is None:
                logger.debug("no timestamp, set to current time")
                self._timestamp = time() * Gst.SECOND
        if not self._playing.is_set():
            return 0
        if not frames:
            return 0

        # https://gstreamer.freedesktop.org/documentation/tutorials/basic/short-cutting-the-pipeline.htm
        duration = Gst.util_uint64_scale(
            num_frames, Gst.SECOND, 44100
        )

        if self._is_music_delivery_too_fast(duration):
            logger.debug("music delivery too fast")
            return 0

        buffer = Gst.Buffer.new_wrapped(bytes(frames))
        with self._timestamp_lock:
            buffer.pts = self._timestamp
            buffer.duration = duration
            self._timestamp += duration

        if self._appsrc.emit("push-buffer", buffer) == Gst.FlowReturn.OK:
            return num_frames
        return 0

    def _is_music_delivery_too_fast(self, duration):
        with self._timestamp_lock:
            return self._timestamp + duration > time() * Gst.SECOND

    def _create_pipeline(self, hlssink2_options):
        pipeline = Gst.Pipeline()

        appsrc = Gst.ElementFactory.make("appsrc")
        appsrc.set_property("caps", Gst.Caps.from_string(self.GST_CAPS))
        appsrc.set_property("format", "time")

        audioconvert = Gst.ElementFactory.make("audioconvert")

        faac = Gst.ElementFactory.make("faac")

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
        pipeline.add(appsrc, audioconvert, faac, sink)

        appsrc.link(audioconvert)
        audioconvert.link(faac)
        faac.link(sink)

        return pipeline, appsrc
