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
        yield from tuple(history)
        del history[0]
