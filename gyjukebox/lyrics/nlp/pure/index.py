import collections
import sqlite3
from pathlib import Path


class TermsWriter:
    def start(self, doc_id):
        raise NotImplementedError

    def add_term(self, term):
        raise NotImplementedError

    def finish(self):
        raise NotImplementedError


class InMemoryTermsWriter(TermsWriter):
    def __init__(self):
        self._current_doc_id = None
        self._current_freqs = None
        # key: term
        self._terms = {}
        # key: doc_id
        self._mags = {}

    def start(self, doc_id):
        self._current_doc_id = doc_id
        self._current_freqs = collections.defaultdict(int)

    def add_term(self, term):
        if self._current_doc_id is None:
            raise ValueError("call add_term before calling start method")
        self._current_freqs[term] += 1

    @property
    def terms(self):
        return self._terms

    @property
    def mags(self):
        return self._mags

    def finish(self):
        mag = 0
        for term, freq in self._current_freqs.items():
            mag += freq ** 2
            terms = self._terms.get(term)
            if terms is None:
                terms = {}
            terms[self._current_doc_id] = freq
            self._terms[term] = terms
        mag **= 0.5
        self._mags[self._current_doc_id] = mag
        self._current_doc_id = None
        self._current_freqs = None


class FileTermsWriter(TermsWriter):
    def __init__(self, index_path, filename="terms.db"):
        self._current_doc_id = None
        self._current_freqs = None
        self._db_path = Path(index_path) / filename
        self._init_db()
        self._conn = sqlite3.connect(self._db_path)

    def _init_db(self):
        conn = sqlite3.connect(self._db_path)
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS terms (term TEXT, doc_id INTEGER, freq INTEGER, PRIMARY KEY (term, doc_id))"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS mags (doc_id INTEGER PRIMARY KEY, mag REAL)"
        )
        conn.commit()
        conn.close()

    def start(self, doc_id):
        self._current_doc_id = doc_id
        self._current_freqs = collections.defaultdict(int)

    def add_term(self, term):
        if self._current_doc_id is None:
            raise ValueError("call add_term before calling start method")
        self._current_freqs[term] += 1

    def finish(self):
        c = self._conn.cursor()
        mag = 0
        for term, freq in self._current_freqs.items():
            mag += freq ** 2
            c.execute(
                "INSERT INTO terms VALUES (?, ?, ?)", (term, self._current_doc_id, freq)
            )
        mag **= 0.5
        c.execute("INSERT INTO mags VALUES (?, ?)", (self._current_doc_id, mag))
        self._current_doc_id = None
        self._current_freqs = None

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()


class TermsReader:
    def get_doc_ids(self, term):
        raise NotImplementedError

    def get_doc_term_freq(self, term, doc_id):
        raise NotImplementedError

    def get_doc_mag(self, doc_id):
        raise NotImplementedError


class InMemoryTermsReader(TermsReader):
    def __init__(self, terms, mags):
        self._terms = terms
        self._mags = mags

    def get_doc_ids(self, term):
        if term not in self._terms:
            return ()
        return self._terms[term]

    def get_doc_term_freq(self, term, doc_id):
        try:
            return self._terms[term][doc_id]
        except KeyError:
            return 0

    def get_doc_mag(self, doc_id):
        return self._mags[doc_id]


class FileTermsReader(TermsReader):
    def __init__(self, index_path, filename="terms.db"):
        db_path = Path(index_path) / filename
        self._conn = sqlite3.connect(db_path)

    def get_doc_ids(self, term):
        c = self._conn.cursor()
        c.execute("SELECT doc_id FROM terms WHERE term=?", (term,))
        for (doc_id,) in c.fetchall():
            yield doc_id

    def get_doc_term_freq(self, term, doc_id):
        c = self._conn.cursor()
        c.execute("SELECT freq FROM terms WHERE term=? AND doc_id=?", (term, doc_id))
        (freq,) = c.fetchone() or (0,)
        return freq

    def get_doc_mag(self, doc_id):
        c = self._conn.cursor()
        c.execute("SELECT mag FROM mags WHERE doc_id=?", (doc_id,))
        (freq,) = c.fetchone()
        return freq


class Indexer:
    def index(self, docs, terms_writer):
        for i, doc in enumerate(docs):
            doc_tokens = docs.analysis(doc)
            terms_writer.start(i)
            for token in set(doc_tokens):
                terms_writer.add_term(token)
            terms_writer.finish()
