import itertools
from gyjukebox.lyrics.ucd import get_wordbreak_mappings


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
