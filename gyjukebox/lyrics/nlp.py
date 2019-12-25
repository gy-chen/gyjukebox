"""NLP tools for searching track title and artist

"""
import collections
import itertools
import string
import math
import json
import linecache
import functools
import pickle
import pathlib
import zlib
import numpy as np
from gyjukebox.lyrics.ucd import get_wordbreak_mappings

IndexPerDocument = collections.namedtuple("IndexPerDocument", "vector")
IndexData = collections.namedtuple("IndexData", "tokens df inverted_index")


class IndexPerDocumentReader:
    def get(self, i):
        raise NotImplementedError


class InMemoryPerDocumentReader:
    def __init__(self, index_per_documents):
        self._index_per_documents = index_per_documents

    def get(self, i):
        return self._index_per_documents[i]


class FilePerDocumentReader:
    def __init__(self, path):
        self._path = pathlib.Path(path)

    def get(self, i):
        with open(self._path / str(i), "rb") as f:
            return pickle.loads(zlib.decompress(f.read()))


class IndexPerDocumentWriter:
    def write(self, index_per_document):
        raise NotImplementedError


class InMemoryPerDocumentWriter:
    def __init__(self):
        self._index_per_documents = []

    def write(self, index_per_document):
        self._index_per_documents.append(index_per_document)

    @property
    def index_per_documents(self):
        return self._index_per_documents


class FilePerDocumentWriter:
    def __init__(self, path):
        self._path = pathlib.Path(path)
        self._no = 0

    def write(self, index_per_document):
        with open(self._path / str(self._no), "wb") as f:
            compressed = zlib.compress(pickle.dumps(index_per_document), 2)
            f.write(compressed)
        self._no += 1


class Scorer:
    def score(self, vec1, vec2):
        raise NotImplementedError


class CosineSimScorer:
    def score(self, vec1, vec2):
        dot_prod = np.sum(vec1 * vec2)

        mag1 = np.sqrt(np.sum(vec1 ** 2))
        mag2 = np.sqrt(np.sum(vec2 ** 2))

        if mag1 == 0 or mag2 == 0:
            return 0

        return dot_prod / (mag1 * mag2)


class Docs:
    def get(self, i):
        raise NotImplementedError

    def analysis(self, doc):
        raise NotImplementedError

    def score(self, doc1, doc2):
        """score similarity of the two docs

        Args:
            doc1 (str|list): str or vector list
            doc2 (str|list): str or vector list

        Returns:
            score number
        """
        raise NotImplementedError

    def vector(self, doc):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError


class JsonLineFileDocs(Docs):
    def __init__(self, path):
        self._path = path

    def get(self, i):
        raw_content = linecache.getline(self._path, i)
        return json.loads(raw_content)

    def __iter__(self):
        with open(self._path, "r") as f:
            for raw_content in f:
                yield json.loads(raw_content)


class LyricsDocs(JsonLineFileDocs):
    def __init__(self, path, vectorizer=None):
        super().__init__(path)
        self._vectorizer = vectorizer
        self._scorer = CosineSimScorer()
        self._title_docs = LyricsTitleDocs(self, vectorizer)
        self._artist_docs = LyricsArtistDocs(self, vectorizer)

    def analysis(self, doc):
        return self._title_docs.analysis(doc["title"]) + self._artist_docs.analysis(
            doc["artist"]
        )

    def _get_field(self, doc, fieldname):
        if isinstance(doc, IndexPerDocument):
            return doc.vector[fieldname]
        return doc[fieldname]

    def score(self, doc1, doc2):
        doc1_title = self._get_field(doc1, "title")
        doc1_artist = self._get_field(doc1, "artist")

        doc2_title = self._get_field(doc2, "title")
        doc2_artist = self._get_field(doc2, "artist")
        return self._title_docs.score(doc1_title, doc2_title) + self._artist_docs.score(
            doc1_artist, doc2_artist
        )

    def vector(self, doc):
        title_vector = self._title_docs.vector(doc["title"])
        artist_vector = self._artist_docs.vector(doc["artist"])
        return {"title": title_vector, "artist": artist_vector}


class LyricsTitleDocs:
    def __init__(
        self, lyrics_docs, vectorizer=None, pipeline=None, scorer=None,
    ):
        self._lyrics_docs = lyrics_docs
        self._vectorizer = vectorizer
        self._pipeline = pipeline
        self._scorer = scorer
        if pipeline is None:
            self._pipeline = ShortTextPipeline()
        if scorer is None:
            self._scorer = CosineSimScorer()

    def get(self, i):
        return self._lyrics_docs.get(i)["title"]

    def analysis(self, doc):
        return self._pipeline.analysis(doc)

    def score(self, doc1, doc2):
        doc1_vec = self.vector(doc1)
        doc2_vec = self.vector(doc2)
        return self._scorer.score(doc1_vec, doc2_vec)

    def vector(self, doc):
        if isinstance(doc, str):
            return self._vectorizer.vectorize(self.analysis(doc))
        return doc

    def __iter__(self):
        return (lyrics["title"] for lyrics in self._lyrics_docs)


class LyricsArtistDocs:
    def __init__(
        self, lyrics_docs, vectorizer=None, pipeline=None, scorer=None,
    ):
        self._lyrics_docs = lyrics_docs
        self._vectorizer = vectorizer
        self._pipeline = pipeline
        self._scorer = scorer
        if pipeline is None:
            self._pipeline = ShortTextPipeline()
        if scorer is None:
            self._scorer = CosineSimScorer()

    def get(self, i):
        return self._lyrics_docs.get(i)["artist"]

    def analysis(self, doc):
        return self._pipeline.analysis(doc)

    def score(self, doc1, doc2):
        doc1_vec = self.vector(doc1)
        doc2_vec = self.vector(doc2)
        return self._scorer.score(doc1_vec, doc2_vec)

    def vector(self, doc):
        if isinstance(doc, str):
            return self._vectorizer.vectorize(self.analysis(doc))
        return doc

    def __iter__(self):
        return (lyrics["artist"] for lyrics in self._lyrics_docs)


class ShortTextPipeline:
    """NLP pipeline for short text like track title or track artist

    1. tokenize using wordbreak
    2. remove punctuation, whitespace
    3. lowercase
    4. ngrams
    5. collect tokens and convert data to bow vectors
    """

    def __init__(self, n=1):
        self._pw_remove_table = str.maketrans(
            "", "", string.punctuation + string.whitespace
        )
        self._n = n

    def analysis(self, doc):
        doc_tokens = tuple(ngrams(self._doc_pre_pipeline(doc), self._n))
        return doc_tokens

    def _doc_pre_pipeline(self, doc):
        """Partial pipeline for preprocessing raw doc

        1. tokenize using wordbreak
        2. remove punctuation, whitespace
        3. lowercase
        """

        for token in words(doc):
            token = token.translate(self._pw_remove_table)
            token = token.lower()
            if not token:
                continue
            yield token


class Indexer:
    def __init__(self, max_df=1.0, min_df=0.0):
        self._max_df = max_df
        self._min_df = min_df

    def index(self, docs):
        tokens = set()
        df = collections.defaultdict(int)
        # map from term to doc
        inverted_index = collections.defaultdict(set)
        docs_len = 0
        for i, doc in enumerate(docs):
            doc_tokens = docs.analysis(doc)
            tf = collections.defaultdict(int)
            for token in doc_tokens:
                tf[token] += 1
                inverted_index[token].add(i)
            for token in tf:
                tf[token] /= len(doc_tokens)
            for token in set(doc_tokens):
                df[token] += 1
                tokens.add(token)
            docs_len += 1

        if self._min_df > 0 or self._max_df < 1.0:
            dfn = {k: v / docs_len for k, v in df.items()}
            tokens = (
                token
                for token in tokens
                if dfn[token] > self._min_df and dfn[token] < self._max_df
            )

        return IndexData(sorted(tokens), df, inverted_index)

    def index_per_documents(self, docs, index_data, index_per_documents_writer):
        for doc in docs:
            vector = docs.vector(doc)
            index_per_document = IndexPerDocument(vector)
            index_per_documents_writer.write(index_per_document)


class Vectorizer:
    def __init__(self, index_data):
        self._index_data = index_data
        self._pos_map = {k: v for v, k in enumerate(index_data.tokens)}

    def vectorize(self, tokens):
        if self._index_data is None:
            raise ValueError("Please load index data")
        vec = np.zeros((len(self._index_data.tokens,)))
        for token in tokens:
            try:
                vec[self._pos_map[token]] += 1
            except KeyError:
                continue
        vec /= self._index_data.df[token]
        return vec


class Searcher:
    def __init__(self, docs, index_data, index_per_document_reader):
        self._docs = docs
        self._index_data = index_data
        self._index_per_document_reader = index_per_document_reader

    def search(self, doc, n=10):
        """Search top docs that matching speciftheic doc

        Args:
            doc (str)
            n (int)

        Returns:
            ((i, score), ...), i is the index that can retrieve original doc back 
        """
        doc_tokens = self._docs.analysis(doc)

        search_doc_indexes = set()
        for doc_token in doc_tokens:
            try:
                search_doc_indexes.update(self._index_data.inverted_index[doc_token])
            except IndexError:
                continue

        search_doc_indexes = list(search_doc_indexes)
        doc_vec = self._docs.vector(doc)
        search_scores = [
            self._docs.score(doc_vec, self._index_per_document_reader.get(i))
            for i in search_doc_indexes
        ]
        search_i = np.argsort(search_scores)
        return [(search_doc_indexes[i], search_scores[i]) for i in search_i[::-1][:n]]


def ngrams(sequence, n):
    """ngrams

    Args:
        sequence (iterable)
        n (int)

    Returns:
        yield ngrams result
    """
    # implementation from nltk
    sequence = iter(sequence)
    history = []
    for _ in range(n - 1):
        try:
            next_item = next(sequence)
        except StopIteration:
            return
        history.append(next_item)
    for item in sequence:
        history.append(item)
        yield tuple(history)
        del history[0]


def words(text, wb_mapping=None):
    if wb_mapping is None:
        wb_mapping = get_wordbreak_mappings()
    cache = []
    pairs = itertools.zip_longest(
        itertools.chain([None, None, None, None], text),
        itertools.chain([None, None, None], text),
        itertools.chain([None, None], text),
        itertools.chain([None], text),
        text,
        text[1:],
    )

    def cache_result(cache):
        try:
            result = "".join(filter(lambda x: x, cache))
            if result:
                yield result
        finally:
            cache.clear()

    for ppp, pp, p, c, n, nn in pairs:
        if _wb1(c, n, wb_mapping):
            yield from cache_result(cache)
            cache.append(n)
        elif _wb2(c, n, wb_mapping):
            yield from cache_result(cache)
        elif _wb3(c, n, wb_mapping):
            cache.append(n)
        elif _wb3a(c, n, wb_mapping):
            yield from cache_result(cache)
            cache.append(n)
        elif _wb3b(c, n, wb_mapping):
            yield from cache_result(cache)
            cache.append(n)
        elif _wb3c(c, n, wb_mapping):
            cache.append(n)
        elif _wb3d(c, n, wb_mapping):
            cache.append(n)
        elif _wb4(c, n, wb_mapping):
            pass
        elif _wb5(c, n, wb_mapping):
            cache.append(n)
        elif _wb6(c, n, nn, wb_mapping):
            cache.append(n)
        elif _wb7(p, c, n, wb_mapping):
            cache.append(n)
        elif _wb7a(c, n, wb_mapping):
            cache.append(n)
        elif _wb7b(c, n, nn, wb_mapping):
            cache.append(n)
        elif _wb7c(p, c, n, wb_mapping):
            cache.append(n)
        elif _wb8(c, n, wb_mapping):
            cache.append(n)
        elif _wb9(c, n, wb_mapping):
            cache.append(n)
        elif _wb10(c, n, wb_mapping):
            cache.append(n)
        elif _wb11(p, c, n, wb_mapping):
            cache.append(n)
        elif _wb12(c, n, nn, wb_mapping):
            cache.append(n)
        elif _wb13(c, n, wb_mapping):
            cache.append(n)
        elif _wb13a(c, n, wb_mapping):
            cache.append(n)
        elif _wb13b(c, n, wb_mapping):
            cache.append(n)
        elif _wb16(ppp, pp, p, c, n, wb_mapping):
            cache.append(n)
        elif _wb999(c, n, wb_mapping):
            yield from cache_result(cache)
            cache.append(n)
        else:
            assert False


def _AHLetter(c, wb_mapping):
    return wb_mapping[c] == "ALetter" or wb_mapping[c] == "Hebrew_Letter"


def _MidNumLetQ(c, wb_mapping):
    return wb_mapping[c] == "MidNumLet" or wb_mapping[c] == "Single_Quote"


def _wb1(c, n, wb_mapping):
    return c is None


def _wb2(c, n, wb_mapping):
    return n is None


def _wb3(c, n, wb_mapping):
    return wb_mapping[c] == "CR" and wb_mapping[n] == "LF"


def _wb3a(c, n, wb_mapping):
    return wb_mapping[c] == "Newline" or wb_mapping[c] == "CR" or wb_mapping[c] == "LF"


def _wb3b(c, n, wb_mapping):
    return wb_mapping[n] == "Newline" or wb_mapping[n] == "CR" or wb_mapping[n] == "LF"


def _wb3c(c, n, wb_mapping):
    # TODO need UTS51 http://unicode.org/reports/tr41/tr41-24.html#UTS51
    return False


def _wb3d(c, n, wb_mapping):
    return wb_mapping[c] == "WSegSpace" and wb_mapping[n] == "WSegSpace"


def _wb4(c, n, wb_mapping):
    # XXX not sure what it means, review this rule later
    return (
        wb_mapping[n] == "Extend" or wb_mapping[n] == "Format" or wb_mapping[n] == "ZWJ"
    )


def _wb5(c, n, wb_mapping):
    return _AHLetter(c, wb_mapping) and _AHLetter(n, wb_mapping)


def _wb6(c, n, nn, wb_mapping):
    return (
        _AHLetter(c, wb_mapping)
        and (wb_mapping[n] == "MidLetter" or _MidNumLetQ(n, wb_mapping))
        and _AHLetter(nn, wb_mapping)
    )


def _wb7(p, c, n, wb_mapping):
    return (
        _AHLetter(p, wb_mapping)
        and (wb_mapping[c] == "MidLetter" or _MidNumLetQ(c, wb_mapping))
        and _AHLetter(n, wb_mapping)
    )


def _wb7a(c, n, wb_mapping):
    return wb_mapping[c] == "Hebrew_Letter" and wb_mapping[n] == "Single_Quote"


def _wb7b(c, n, nn, wb_mapping):
    return (
        wb_mapping[c] == "Hebrew_Letter"
        and wb_mapping[n] == "Double_Quote"
        and wb_mapping[nn] == "Hebrew_Letter"
    )


def _wb7c(p, c, n, wb_mapping):
    return (
        wb_mapping[p] == "Hebrew_Letter"
        and wb_mapping[c] == "Double_Quote"
        and wb_mapping[n] == "Hebrew_Letter"
    )


def _wb8(c, n, wb_mapping):
    return wb_mapping[c] == "Numeric" and wb_mapping[n] == "Numeric"


def _wb9(c, n, wb_mapping):
    return _AHLetter(c, wb_mapping) and wb_mapping[n] == "Numeric"


def _wb10(c, n, wb_mapping):
    return wb_mapping[c] == "Numeric" and _AHLetter(n, wb_mapping)


def _wb11(p, c, n, wb_mapping):
    return (
        wb_mapping[p] == "Numeric"
        and (wb_mapping[c] == "MidNum" or _MidNumLetQ(c, wb_mapping))
        and wb_mapping[n] == "Numeric"
    )


def _wb12(c, n, nn, wb_mapping):
    return (
        wb_mapping[c] == "Numeric"
        and (wb_mapping[n] == "MidNum" or _MidNumLetQ(n, wb_mapping))
        and wb_mapping[nn] == "Numeric"
    )


def _wb13(c, n, wb_mapping):
    return wb_mapping[c] == "Katakana" and wb_mapping[n] == "Katakana"


def _wb13a(c, n, wb_mapping):
    return (
        _AHLetter(c, wb_mapping)
        or wb_mapping[c] == "Numeric"
        or wb_mapping[c] == "Katakana"
        or wb_mapping[c] == "ExtendNumLet"
    ) and wb_mapping[n] == "ExtendNumLet"


def _wb13b(c, n, wb_mapping):
    return wb_mapping[c] == "ExtendNumLet" and (
        _AHLetter(n, wb_mapping)
        or wb_mapping[n] == "Numeric"
        or wb_mapping[n] == "Katakana"
    )


def _wb16(ppp, pp, p, c, n, wb_mapping):
    if (
        wb_mapping[ppp] != "RI"
        and wb_mapping[pp] == "RI"
        and wb_mapping[p] == "RI"
        and wb_mapping[c] == "RI"
        and wb_mapping[n] == "RI"
    ):
        return True
    return wb_mapping[p] != "RI" and wb_mapping[c] == "RI" and wb_mapping[n] == "RI"


def _wb999(c, n, wb_mapping):
    return True


# TODO remove me later
if __name__ == "__main__":
    docs = LyricsDocs("mojim.jl")
    indexer = Indexer(0.04)
    index_data = indexer.index(docs)
    vectorizer = Vectorizer(index_data)
    docs = LyricsDocs("mojim.jl", vectorizer)
    index_per_document_writer = FilePerDocumentWriter("demo_index")
    indexer.index_per_documents(docs, vectorizer, index_per_document_writer)
    index_per_document_reader = FilePerDocumentReader("demo_index")
    print("#### indexed")
    searcher = Searcher(docs, index_data, index_per_document_reader)
    result = searcher.search({"artist": "ari supply", "title": "all out of love"})
    print(result)
    for i, score in result:
        print(score)
        print(docs.get(i))
