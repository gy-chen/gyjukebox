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

    def score(self, doc1, doc2):
        """score similarity of the two docs

        Args:
            doc1 (gyjukebox.lyrics.nlp.pure.index.IndexPerDocument)
            doc2 (gyjukebox.lyrics.nlp.pure.index.IndexPerDocument)

        Returns:
            score number
        """
        raise NotImplementedError

    def index(self, doc):
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

    def score(self, index_per_document_1, index_per_document_2):
        doc1_title = index_per_document_1["title"]
        doc1_artist = index_per_document_1["artist"]

        doc2_title = index_per_document_2["title"]
        doc2_artist = index_per_document_2["artist"]
        return self._title_docs.score(doc1_title, doc2_title) + self._artist_docs.score(
            doc1_artist, doc2_artist
        )

    def index(self, doc):
        return {
            "title": self._title_docs.index(doc["title"]),
            "artist": self._artist_docs.index(doc["artist"]),
        }


class LyricsTitleDocs:
    def __init__(self, lyrics_docs):
        self._lyrics_docs = lyrics_docs
        self._pipeline = ShortTextPipeline()
        self._scorer = CosineSimScorer()

    def get(self, i):
        return self._lyrics_docs.get(i)["title"]

    def analysis(self, doc):
        return self._pipeline.analysis(doc)

    def score(self, index_per_document_1, index_per_document_2):
        doc1_bow = index_per_document_1["bow"]
        doc1_mag = index_per_document_1["mag"]
        doc2_bow = index_per_document_2["bow"]
        doc2_mag = index_per_document_2["mag"]
        return self._scorer.score(doc1_bow, doc1_mag, doc2_bow, doc2_mag)

    def _bow(self, doc):
        return collections.Counter(self.analysis(doc))

    def _mag(self, bow):
        mag = 0
        for freq in bow.values():
            mag += freq ** 2
        return math.sqrt(mag)

    def index(self, doc):
        bow = self._bow(doc)
        return {"bow": bow, "mag": self._mag(bow)}

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

    def score(self, index_per_document_1, index_per_document_2):
        doc1_bow = index_per_document_1["bow"]
        doc1_mag = index_per_document_1["mag"]
        doc2_bow = index_per_document_2["bow"]
        doc2_mag = index_per_document_2["mag"]
        return self._scorer.score(doc1_bow, doc1_mag, doc2_bow, doc2_mag)

    def _bow(self, doc):
        return collections.Counter(self.analysis(doc))

    def _mag(self, bow):
        mag = 0
        for freq in bow.values():
            mag += freq ** 2
        return math.sqrt(mag)

    def index(self, doc):
        bow = self._bow(doc)
        return {"bow": bow, "mag": self._mag(bow)}

    def __iter__(self):
        return (lyrics["artist"] for lyrics in self._lyrics_docs)
