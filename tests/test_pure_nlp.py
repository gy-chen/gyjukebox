import tempfile
import pathlib
import pytest
from gyjukebox.lyrics.nlp.pure.index import Indexer
from gyjukebox.lyrics.nlp.pure.index import FileIndexDataWriter
from gyjukebox.lyrics.nlp.pure.index import FileIndexDataReader
from gyjukebox.lyrics.nlp.pure.index import FileIndexPerDocumentWriter
from gyjukebox.lyrics.nlp.pure.index import FileIndexPerDocumentReader
from gyjukebox.lyrics.nlp.pure.search import Searcher
from gyjukebox.lyrics.nlp.pure.docs import LyricsDocs
from gyjukebox.lyrics.nlp.pure.scorer import Vectorizer
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
    index_data_writer = FileIndexDataWriter(index_dir)
    indexer = Indexer(0.05)
    indexer.index(docs, index_data_writer)

    index_data_reader = FileIndexDataReader(index_dir)
    vectorizer = Vectorizer(index_data_reader.get())
    docs = LyricsDocs(lyrics_path, vectorizer)
    index_per_documents_writer = FileIndexPerDocumentWriter(index_dir)
    indexer.index_per_documents(
        docs, index_data_reader.get(), index_per_documents_writer
    )

    index_per_document_reader = FileIndexPerDocumentReader(index_dir)
    searcher = Searcher(docs, index_data_reader, index_per_document_reader)
    searcher.search({"artist": "air", "title": "love"})


def test_pure_nlp_searcher(index_dir, lyrics_path):
    pure_nlp_searcher = PureNlpLyricsSearcher(lyrics_path, index_dir)
    result = pure_nlp_searcher.search("air", "love")
    assert result.artist == "Air Supply"
    assert result.title == "All Out Of Love"
