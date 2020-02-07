import collections
import linecache
import json
import math
from gyjukebox.lyrics.nlp.pure.scorer import CosineSimScorer
from gyjukebox.lyrics.nlp.pure.pipeline import ShortTextPipeline


class Docs:
    def get(self, i):
        raise NotImplementedError

    def analysis(self, doc):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError


class JsonLineFileDocs(Docs):
    def __init__(self, path):
        self._path = path

    def get(self, i):
        raw_content = linecache.getline(self._path, i + 1)
        return json.loads(raw_content)

    def __iter__(self):
        with open(self._path, "r") as f:
            for raw_content in f:
                yield json.loads(raw_content)


class LyricsDocs(JsonLineFileDocs):
    def __init__(self, path):
        super().__init__(path)
        self._title_docs = LyricsTitleDocs(self)
        self._artist_docs = LyricsArtistDocs(self)

    def analysis(self, doc):
        return self._title_docs.analysis(doc["title"]) + self._artist_docs.analysis(
            doc["artist"]
        )


class LyricsTitleDocs:
    def __init__(self, lyrics_docs):
        self._lyrics_docs = lyrics_docs
        self._pipeline = ShortTextPipeline()
        self._scorer = CosineSimScorer()

    def get(self, i):
        return self._lyrics_docs.get(i)["title"]

    def analysis(self, doc):
        return self._pipeline.analysis(doc)

    def __iter__(self):
        return (lyrics["title"] for lyrics in self._lyrics_docs)


class LyricsArtistDocs:
    def __init__(self, lyrics_docs):
        self._lyrics_docs = lyrics_docs
        self._pipeline = ShortTextPipeline()
        self._scorer = CosineSimScorer()

    def get(self, i):
        return self._lyrics_docs.get(i)["artist"]

    def analysis(self, doc):
        return self._pipeline.analysis(doc)

    def __iter__(self):
        return (lyrics["artist"] for lyrics in self._lyrics_docs)
