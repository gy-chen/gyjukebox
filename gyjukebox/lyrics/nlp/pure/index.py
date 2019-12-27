import collections
import linecache
import pathlib
import pickle
import zlib

IndexData = collections.namedtuple("IndexData", "tokens df inverted_index")


class IndexPerDocumentReader:
    def get(self, i):
        raise NotImplementedError


class InMemoryIndexPerDocumentReader(IndexPerDocumentReader):
    def __init__(self, index_per_documents):
        self._index_per_documents = index_per_documents

    def get(self, i):
        return self._index_per_documents[i]


class FileIndexPerDocumentReader(IndexPerDocumentReader):
    def __init__(self, path, index_filename="ipd", toc_filename="ipd_toc"):
        path = pathlib.Path(path)
        self._index_f = open(path / index_filename, "rb")
        self._toc_path = str(path / toc_filename)

    def get(self, i):
        location, length = self._get_location(i)
        self._index_f.seek(location)
        raw_content = self._index_f.read(length)
        return pickle.loads(zlib.decompress(raw_content))

    def close(self):
        self._index_f.close()

    def _get_location(self, i):
        l1 = int(linecache.getline(self._toc_path, i + 1))
        l2 = int(linecache.getline(self._toc_path, i + 2))
        return (l1, l2 - l1)


class IndexPerDocumentWriter:
    def write(self, index_per_document):
        raise NotImplementedError


class InMemoryIndexPerDocumentWriter:
    def __init__(self):
        self._index_per_documents = []

    def write(self, index_per_document):
        self._index_per_documents.append(index_per_document)

    @property
    def index_per_documents(self):
        return self._index_per_documents


class FileIndexPerDocumentWriter:
    def __init__(self, path, index_filename="ipd", toc_filename="ipd_toc"):
        path = pathlib.Path(path)
        self._index_f = open(path / index_filename, "wb")
        self._toc_f = open(path / toc_filename, "w")
        self._acc = 0

    def write(self, index_per_document):
        self._toc_f.write(str(self._acc))
        self._toc_f.write("\n")
        compressed = zlib.compress(pickle.dumps(index_per_document), 2)
        writed = self._index_f.write(compressed)
        self._acc += writed

    def close(self):
        self._index_f.close()
        self._toc_f.close()


class IndexDataReader:
    def get(self):
        raise NotImplementedError


class FileIndexDataReader(IndexDataReader):
    def __init__(self, path, index_filename="index"):
        self._path = pathlib.Path(path)
        self._index_filename = index_filename

    def get(self):
        with open(self._path / self._index_filename, "rb") as f:
            return pickle.load(f)


class IndexDataWriter:
    def write(self, index_data):
        raise NotImplementedError


class FileIndexDataWriter(IndexDataWriter):
    def __init__(self, path, index_filename="index"):
        self._path = pathlib.Path(path)
        self._index_filename = index_filename

    def write(self, index_data):
        with open(self._path / self._index_filename, "wb") as f:
            return pickle.dump(index_data, f)


class Indexer:
    def __init__(self, max_df=1.0, min_df=0.0):
        self._max_df = max_df
        self._min_df = min_df

    def index(self, docs, index_data_writer):
        tokens = set()
        df = collections.defaultdict(int)
        # map from term to doc
        inverted_index = collections.defaultdict(set)
        docs_len = 0
        for i, doc in enumerate(docs):
            doc_tokens = docs.analysis(doc)
            for token in set(doc_tokens):
                inverted_index[token].add(i)
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

        index_data_writer.write(IndexData(sorted(tokens), df, inverted_index))

    def index_per_documents(self, docs, index_data, index_per_documents_writer):
        for doc in docs:
            index_per_document = docs.index(doc)
            index_per_documents_writer.write(index_per_document)
