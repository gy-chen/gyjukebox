import tempfile
import pathlib
import pytest
from gyjukebox.lyrics.nlp.pure.docs import LyricsDocs
from gyjukebox.lyrics.nlp.pure.index import Indexer
from gyjukebox.lyrics.nlp.pure.index import FileTermsWriter
from gyjukebox.lyrics.nlp.pure.index import FileTermsReader
from gyjukebox.lyrics.nlp.pure.search import Searcher
from gyjukebox.lyrics.search import PureNlpLyricsSearcher


@pytest.fixture(scope="module")
def index_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


@pytest.fixture()
def lyrics_path():
    return str(pathlib.Path(__file__).parent / "mojim.jl")


def test_pure_nlp_without_error(index_dir, lyrics_path):
    docs = LyricsDocs(lyrics_path)
    terms_writer = FileTermsWriter(index_dir)
    indexer = Indexer()
    indexer.index(docs, terms_writer)
    terms_writer.commit()
    terms_writer.close()

    terms_reader = FileTermsReader(index_dir)

    searcher = Searcher(docs, terms_reader)
    searcher.search({"artist": "air", "title": "love"})


def test_pure_nlp_searcher(index_dir, lyrics_path):
    pure_nlp_searcher = PureNlpLyricsSearcher(lyrics_path, index_dir)
    result = pure_nlp_searcher.search("air supply", "young love")
    assert result.artist == "Air Supply"
    assert result.title == "Young Love"
