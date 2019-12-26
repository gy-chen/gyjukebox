import string
from gyjukebox.lyrics.nlp.tokenize import words
from gyjukebox.lyrics.nlp.utils import ngrams


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
