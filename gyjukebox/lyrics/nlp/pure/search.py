import numpy as np


class Searcher:
    def __init__(self, docs, index_data_reader, index_per_document_reader):
        self._docs = docs
        self._index_data_reader = index_data_reader
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
        index_data = self._index_data_reader.get()
        for doc_token in doc_tokens:
            try:
                search_doc_indexes.update(index_data.inverted_index[doc_token])
            except IndexError:
                continue

        search_doc_indexes = list(search_doc_indexes)
        doc_index = self._docs.index(doc)
        search_scores = [
            self._docs.score(doc_index, self._index_per_document_reader.get(i))
            for i in search_doc_indexes
        ]
        search_i = np.argsort(search_scores)
        return [(search_doc_indexes[i], search_scores[i]) for i in search_i[::-1][:n]]
