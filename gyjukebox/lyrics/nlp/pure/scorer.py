import numpy as np


class Scorer:
    def score(self, vec1, vec2):
        raise NotImplementedError


class CosineSimScorer(Scorer):
    def score(self, vec1, vec2):
        dot_prod = np.sum(vec1 * vec2)

        mag1 = np.sqrt(np.sum(vec1 ** 2))
        mag2 = np.sqrt(np.sum(vec2 ** 2))

        if mag1 == 0 or mag2 == 0:
            return 0

        return dot_prod / (mag1 * mag2)


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
