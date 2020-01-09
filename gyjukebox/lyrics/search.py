from gyjukebox.lyrics.nlp.pure.docs import LyricsDocs
from gyjukebox.lyrics.nlp.pure.index import FileIndexDataReader
from gyjukebox.lyrics.nlp.pure.index import FileIndexPerDocumentReader
from gyjukebox.lyrics.nlp.pure.search import Searcher
from gyjukebox.lyrics.model import Lyrics


class LyricsSearcher:
    def search(self, artist, title):
        """Search lyrics for given aritst and title

        Args:
            artist (str)
            title (str)

        Returns:
            instance of gyjukebox.lyrics.model.Lyrics or None if no match
        """
        raise NotImplementedError


class PureNlpLyricsSearcher(LyricsSearcher):
    """Lyrics searcher using poor self written nlp tools

    Args:
        lyrics_docs_path (str): path that stored original lyrics content
        index_data_path (str): path that stored indexed lyrics data
    """

    def __init__(self, lyrics_docs_path, index_data_path):
        self._searcher = self._build_searcher(lyrics_docs_path, index_data_path)

    def _build_searcher(self, lyrics_docs_path, index_data_path):
        index_data_reader = FileIndexDataReader(index_data_path)
        docs = LyricsDocs(lyrics_docs_path)
        index_per_document_reader = FileIndexPerDocumentReader(index_data_path)
        return Searcher(docs, index_data_reader, index_per_document_reader)

    def search(self, artist, title):
        doc = {"artist": artist, "title": title}
        result = self._searcher.search(doc, n=1, return_doc=True)
        if not result:
            return None
        lyrics_dict = result[0][0]
        return Lyrics(
            lyrics_dict["title"], lyrics_dict["artist"], lyrics_dict["lyrics"]
        )
