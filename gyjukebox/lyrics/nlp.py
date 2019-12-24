"""NLP tools for searching track title and artist

"""
import collections
import itertools
import string
import math
import json
import linecache
import functools
import numpy as np
from gyjukebox.lyrics.ucd import get_wordbreak_mappings

IndexData = collections.namedtuple("IndexData", "tokens df inverted_index")


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
        self._title_docs = LyricsTitleDocs(self, vectorizer)
        self._artist_docs = LyricsArtistDocs(self, vectorizer)

    def analysis(self, doc):
        return self._title_docs.analysis(doc["title"]) + self._artist_docs.analysis(
            doc["artist"]
        )

    def score(self, doc1, doc2):
        return self._title_docs.score(
            doc1["title"], doc2["title"]
        ) + self._artist_docs.score(doc1["artist"], doc2["artist"])


class LyricsTitleDocs:
    def __init__(self, lyrics_docs, vectorizer=None, pipeline=None, scorer=None):
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

    @functools.lru_cache()
    def analysis(self, doc):
        return self._pipeline.analysis(doc)

    def score(self, doc1, doc2):
        doc1_vec = self._vectorizer.vectorize(self.analysis(doc1))
        doc2_vec = self._vectorizer.vectorize(self.analysis(doc2))
        return self._scorer.score(doc1_vec, doc2_vec)

    def __iter__(self):
        return (lyrics["title"] for lyrics in self._lyrics_docs)


class LyricsArtistDocs:
    def __init__(self, lyrics_docs, vectorizer=None, pipeline=None, scorer=None):
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

    @functools.lru_cache()
    def analysis(self, doc):
        return self._pipeline.analysis(doc)

    def score(self, doc1, doc2):
        doc1_vec = self._vectorizer.vectorize(self.analysis(doc1))
        doc2_vec = self._vectorizer.vectorize(self.analysis(doc2))
        return self._scorer.score(doc1_vec, doc2_vec)

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
        doc_tokens = list(ngrams(self._doc_pre_pipeline(doc), self._n))
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
    def __init__(self, docs, max_df=1.0, min_df=0.0):
        self._docs = docs
        self._max_df = max_df
        self._min_df = min_df
        self._index_data = None

    def index(self):
        tokens = set()
        df = collections.defaultdict(int)
        # map from term to doc
        inverted_index = collections.defaultdict(set)
        docs_len = 0
        for i, doc in enumerate(self._docs):
            doc_tokens = self._docs.analysis(doc)
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

        self._index_data = IndexData(sorted(tokens), df, inverted_index)

    @property
    def index_data(self):
        return self._index_data


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
    def __init__(self, docs, index_data):
        self._docs = docs
        self._index_data = index_data

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
        search_docs = [self._docs.get(i) for i in search_doc_indexes]
        search_scores = [
            self._docs.score(doc, search_doc) for search_doc in search_docs
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
    indexer = Indexer(docs, 0.07)
    indexer.index()
    print("#### indexed")
    index_data = indexer.index_data
    vectorizer = Vectorizer(index_data)
    docs = LyricsDocs("mojim.jl", vectorizer)
    searcher = Searcher(docs, index_data)
    result = searcher.search({"artist": "ari supply", "title": "all out of love"})
    print(result)
    for i, score in result:
        print(score)
        print(docs.get(i))
