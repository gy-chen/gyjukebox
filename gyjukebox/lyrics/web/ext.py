from flask import current_app
from flask import _app_ctx_stack
from gyjukebox.lyrics.nlp.pure.index import Indexer
from gyjukebox.lyrics.nlp.pure.index import FileIndexDataWriter
from gyjukebox.lyrics.nlp.pure.index import FileIndexDataReader
from gyjukebox.lyrics.nlp.pure.index import FileIndexPerDocumentWriter
from gyjukebox.lyrics.nlp.pure.index import FileIndexPerDocumentReader
from gyjukebox.lyrics.nlp.pure.docs import LyricsDocs
from gyjukebox.lyrics.search import PureNlpLyricsSearcher


class LyricsSearchExt:
    def __init__(self, app=None):
        self._app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("LYRICS_SEARCH_LYRICS_PATH", None)
        app.config.setdefault("LYRICS_SEARCH_INDEX_PATH", None)

    def index(self):
        lyrics_path = self.app.config["LYRICS_SEARCH_LYRICS_PATH"]
        index_path = self.app.config["LYRICS_SEARCH_INDEX_PATH"]
        docs = LyricsDocs(lyrics_path)
        index_data_writer = FileIndexDataWriter(index_path)
        indexer = Indexer()
        indexer.index(docs, index_data_writer)

        index_data_reader = FileIndexDataReader(index_path)
        index_data = index_data_reader.get()
        index_per_documents_writer = FileIndexPerDocumentWriter(index_path)
        indexer.index_per_documents(docs, index_data, index_per_documents_writer)

    @property
    def searcher(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "lyrics_search_ext_searcher"):
                lyrics_path = self.app.config["LYRICS_SEARCH_LYRICS_PATH"]
                index_path = self.app.config["LYRICS_SEARCH_INDEX_PATH"]
                ctx.lyrics_search_ext_searcher = PureNlpLyricsSearcher(
                    lyrics_path, index_path
                )
            return ctx.lyrics_search_ext_searcher

    @property
    def app(self):
        return self._app or current_app
