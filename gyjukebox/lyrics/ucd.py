"""Tools for paring ucd data

https://www.unicode.org/Public/12.1.0/ucd/auxiliary/WordBreakProperty.txt
"""
import enum
import collections
import re
import pathlib
import json
import functools
import requests
from gyjukebox.lyrics.util import Peekable

UCD_WORDBREAK_URL = (
    "https://www.unicode.org/Public/12.1.0/ucd/auxiliary/WordBreakProperty.txt"
)
RE_CODEPOINTS = re.compile(r"([A-F0-9]{4,5})(?:..([A-F0-9]{4,5}))?")
WordBreakProperty = collections.namedtuple("WordBreakProperty", "codepoints property")
Token = collections.namedtuple("Token", "type value")


@functools.lru_cache()
def get_wordbreak_mappings(url=UCD_WORDBREAK_URL, use_cache=True):
    """Get and parse ucd wordbreak data

    Args:
        url (str): ucd wordbreak property url, default is https://www.unicode.org/Public/12.1.0/ucd/auxiliary/WordBreakProperty.txt
        use_cache (bool): use parsed wordbreak mapping store in this package directory, default is True

    Returns:
        dict that key is cdepoint, value is wordbreak property
    """
    if not use_cache:
        raw_content = get_ucd_wordbreak_content(url)
        content = parse_text(raw_content)
        return build_mapping(content)
    with open(pathlib.Path(__file__).parent / "wordbreak.json", "r") as f:
        dd = collections.defaultdict(lambda: "Other")
        dd.update(json.load(f))
        return dd


class TokenType(enum.Enum):
    COMMENT = enum.auto()
    PROPERTY = enum.auto()


def tokenize(text):
    text_iter = Peekable(text)
    while True:
        try:
            c = text_iter.peek()
        except StopIteration:
            return
        if c == "#":
            next(text_iter)
            yield _parse_comment_token(text_iter)
        elif c == ";":
            next(text_iter)
        elif c.isspace():
            next(text_iter)
        elif c.isalnum():
            yield _parse_property_token(text_iter)
        else:
            raise ValueError(f"unexpect character: {c}")


def _parse_comment_token(text_iter):
    token_value = ""
    while True:
        try:
            c = next(text_iter)
            if c == "\n":
                break
        except StopIteration:
            break
        token_value += c
    return Token(TokenType.COMMENT, token_value)


def _parse_property_token(text_iter):
    token_value = ""
    try:
        c = next(text_iter)
    except StopIteration:
        raise ValueError("expect property has value")
    while not c.isspace() and c != ";":
        token_value += c
        try:
            c = next(text_iter)
        except StopIteration:
            break
    return Token(TokenType.PROPERTY, token_value)


def parse(tokens):
    tokens_iter = Peekable(tokens)
    while True:
        try:
            token = tokens_iter.peek()
        except StopIteration:
            return
        if token.type == TokenType.COMMENT:
            next(tokens_iter)
        elif token.type == TokenType.PROPERTY:
            yield _parse_wordbreak_property(tokens_iter)
        else:
            raise ValueError(f"unexpect token {token}")


def _parse_wordbreak_property(tokens_iter):
    token = next(tokens_iter)
    codepoints = _parse_codepoints(token.value)

    token = next(tokens_iter)
    property = token.value

    return WordBreakProperty(codepoints, property)


def _parse_codepoints(codepoints):
    match = RE_CODEPOINTS.match(codepoints)
    if not match:
        raise ValueError(f"invalid codepoints: {codepoints}")
    start = _to_codepoint(match.group(1))
    end = _to_codepoint(match.group(2))
    if not end:
        return [start]
    return _codepoints_between(start, end)


def _to_codepoint(codepoint):
    if codepoint is None:
        return None
    return chr(int(codepoint, 16))


def _codepoints_between(start, end):
    return list(map(chr, range(ord(start), ord(end) + 1)))


def get_ucd_wordbreak_content(url=UCD_WORDBREAK_URL):
    r = requests.get(url)
    return r.text


def parse_text(text):
    return parse(tokenize(text))


def build_mapping(word_break_properties):
    result = collections.defaultdict(lambda: "Other")
    for wbp in word_break_properties:
        for codepoint in wbp.codepoints:
            result[codepoint] = wbp.property
    return result
