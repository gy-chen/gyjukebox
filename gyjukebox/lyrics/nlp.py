"""NLP tools for searching track title and artist

"""
import collections
import itertools
import string
import math
import json
import linecache
import numpy as np
from gyjukebox.lyrics.ucd import get_wordbreak_mappings


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


class LyricsTitleFileDocs(JsonLineFileDocs):
    def get(self, i):
        return super().get(i)["title"]

    def __iter__(self):
        return (lyrics["title"] for lyrics in super().__iter__())


class ShortTextPipeline:
    """NLP pipeline for short text like track title or track artist

    1. tokenize using wordbreak
    2. remove punctuation, whitespace
    3. lowercase
    4. ngrams
    5. remove some tokens using max df and min df
    6. collect tokens and convert data to bow vectors
    """

    def __init__(self, docs, max_df=1.0, min_df=0.0, n=1, scorer=CosineSimScorer()):
        self._pw_remove_table = str.maketrans(
            "", "", string.punctuation + string.whitespace
        )
        self._docs = docs
        self._max_df = max_df
        self._min_df = min_df
        self._n = n
        self._scorer = scorer
        self.tokens = None
        self.df = None
        # map from term to doc
        self.inverted_index = None

    def load(self, tokens, df, inverted_index):
        self.tokens = tokens
        self.df = df
        self.inverted_index = inverted_index

    def index(self):
        tokens = set()
        df = collections.defaultdict(int)
        inverted_index = collections.defaultdict(set)
        docs_len = 0
        for i, doc in enumerate(self._docs):
            doc_tokens = list(ngrams(self._doc_pre_pipeline(doc), self._n))
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

        self.tokens = sorted(tokens)
        self.df = df
        self.inverted_index = inverted_index

    def analysis(self, doc):
        if self.tokens is None or self.df is None:
            raise ValueError(
                "Please run index first, or load saved tokens and df state."
            )
        doc_tokens = list(ngrams(self._doc_pre_pipeline(doc), self._n))
        vec = np.zeros((len(self.tokens,)))
        for token, freq in collections.Counter(doc_tokens).items():
            try:
                i = self.tokens.index(token)
                vec[i] = (freq / len(doc_tokens)) / self.df[token]
            except ValueError:
                continue
        return vec

    def search(self, doc):
        doc_tokens = ngrams(self._doc_pre_pipeline(doc), self._n)

        search_doc_indexes = set()
        for doc_token in doc_tokens:
            try:
                search_doc_indexes.update(self.inverted_index[doc_token])
            except IndexError:
                continue

        search_docs = [self._docs.get(i) for i in search_doc_indexes]
        doc_vec = self.analysis(doc)
        search_scores = [
            self._scorer.score(doc_vec, self.analysis(search_doc))
            for search_doc in search_docs
        ]
        search_i = np.argsort(search_scores)
        return search_docs[search_i[-1]]

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
    pipeline = ShortTextPipeline(LyricsTitleFileDocs("mojim.jl"), 0.07)
    pipeline.index()
    print("#### indexed")
    print(pipeline.search("All out of love"))
