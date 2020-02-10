import collections
import heapq
from gyjukebox.lyrics.nlp.pure.scorer import CosineSimScorer


class Searcher:
    def __init__(self, docs, terms_reader):
        self._docs = docs
        self._terms_reader = terms_reader
        self._scorer = CosineSimScorer()

    def _score(self, token_freqs, doc2_id):
        mag1 = 0
        mag2 = self._terms_reader.get_doc_mag(doc2_id)
        bow1 = {}
        bow2 = {}
        for token, freq in token_freqs.items():
            mag1 += freq ** 2
            bow1[token] = freq
            bow2[token] = self._terms_reader.get_doc_term_freq(token, doc2_id)
        return self._scorer.score(bow1, mag1, bow2, mag2)

    def search(self, doc, n=10, return_doc=False):
        """Search top docs that matching speciftheic doc

        Args:
            doc (str)
            n (int)

        Returns:
            ((i, score), ...), i is the index that can retrieve original doc back 
            ((doc, score), ...), if return_doc is True
        """
        doc_token_freqs = collections.Counter(self._docs.analysis(doc))

        search_doc_id_freqs = collections.defaultdict(int)
        for doc_token in doc_token_freqs.keys():
            for doc_id in self._terms_reader.get_doc_ids(doc_token):
                search_doc_id_freqs[doc_id] += 1

        search_doc_id_freqs = sorted(
            (
                (freq, -self._terms_reader.get_doc_mag(doc_id), doc_id)
                for doc_id, freq in search_doc_id_freqs.items()
            ),
            reverse=True,
        )
        search_doc_ids = []
        while len(search_doc_ids) < n and search_doc_id_freqs:
            search_doc_ids.append(search_doc_id_freqs.pop(0)[2])

        heap = []
        for i in search_doc_ids:
            score = self._score(doc_token_freqs, i)
            heapq.heappush(heap, (-score, i))
        transform = self._docs.get if return_doc else lambda i: i
        result = []
        for _ in range(min(len(heap), n)):
            score, i = heapq.heappop(heap)
            result.append((transform(i), -score))
        return result
